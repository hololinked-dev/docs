from hololinked.server import Property, Thing
from typing import Annotated, Tuple
from pydantic import BaseModel, Field
from pyueye import ueye


class Rect(BaseModel):
    x : Annotated[int, Field(default=0, ge=0)]
    y : Annotated[int, Field(default=0, ge=0)]
    width : Annotated[int, Field(default=0, gt=0)]
    height: Annotated[int, Field(default=0, gt=0)]


class UEyeCamera(Thing):
    def get_aoi(self) -> Rect:
        """Get current AOI from camera as Rect class (with .x, .y, .width, .height)."""
        rect_aoi = ueye.IS_RECT()
        ret = ueye.is_AOI(self.handle, ueye.IS_AOI_IMAGE_GET_AOI,
                        rect_aoi, ueye.sizeof(rect_aoi))
        assert return_code_OK(self.handle, ret)
        return Rect(
                x=rect_aoi.s32X.value,
                y=rect_aoi.s32Y.value,
                width=rect_aoi.s32Width.value,
                height=rect_aoi.s32Height.value
            )

    def set_aoi(self, value: Rect):
        """Set camera AOI. Specify as x,y,width,height or a tuple
        (x,y,width,height) or as Rect object."""
        rect_aoi = ueye.IS_RECT()
        rect_aoi.s32X = ueye.int(value.x)
        rect_aoi.s32Y = ueye.int(value.y)
        rect_aoi.s32Width = ueye.int(value.width)
        rect_aoi.s32Height = ueye.int(value.height)

        ret = ueye.is_AOI(self.handle, ueye.IS_AOI_IMAGE_SET_AOI,
                             rect_aoi, ueye.sizeof(rect_aoi))
        assert return_code_OK(self.handle, ret)


    AOI = Property(fget=get_aoi, fset=set_aoi, doc="Area of interest", 
                model=Rect) # type: Rect




trigger_schema = {
    'type': 'object',
    'properties' : {
        'enabled' : { 'type': 'boolean' },
        'channel' : { 
            'type': 'string', 
            'enum': ['A', 'B', 'C', 'D', 'EXTERNAL', 'AUX'] 
            # include both external and aux for 5000 & 6000 series
            # let the device driver will check if the channel is valid for the series
        },
        'threshold' : { 'type': 'number' },
        'adc' : { 'type': 'boolean' },
        'direction' : { 
            'type': 'string', 
            'enum': ['above', 'below', 'rising', 'falling', 'rising_or_falling'] 
        },
        'delay' : { 'type': 'integer' },
        'auto_trigger' : { 
            'type': 'integer', 
            'minimum': 0 
        }
    }
}

class Picoscope(Thing):

    trigger = Property(default=0, doc="Trigger settings",
                    model=trigger_schema) # type: dict
    
    @trigger.setter
    def set_trigger(self, value) -> None:
        enabled = ct.c_int16(int(value["enabled"]))
        direction = ps.PS6000_THRESHOLD_DIRECTION['PS6000_{}'.format(
                                                 value["direction"].upper())]
        ch = channel.upper()
        if channel.upper() in ['A', 'B', 'C', 'D']:
            channel = ps.PS6000_CHANNEL['PS6000_CHANNEL_{}'.format(
                                        channel.upper())]
        else:
            channel = ps.PS6000_CHANNEL['PS6000_TRIGGER_AUX']
        if not value["adc"]:
            if channel in ['A', 'B', 'C', 'D']:
                threshold = int(threshold * self.max_adc * 1e3
                            / self.ranges[self.channel_settings[ch]['v_range']])
                # print(threshold)
            else:
                threshold = int(self.max_adc/5)
        threshold = ct.c_int16(threshold)
        auto_trigger = ct.c_int16(int(auto_trigger))
        self._status['trigger'] = ps.ps6000SetSimpleTrigger(self._ct_handle,
                                    enabled, channel, threshold, direction, 
                                    delay, auto_trigger)
        assert_pico_ok(self._status['trigger'])