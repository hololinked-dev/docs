from hololinked.core import Property, Thing
from typing import Annotated, Tuple
from pydantic import BaseModel, Field
from pyueye import ueye


class Rect(BaseModel):
    x: Annotated[int, Field(default=0, ge=0)]
    y: Annotated[int, Field(default=0, ge=0)]
    width: Annotated[int, Field(default=0, gt=0)]
    height: Annotated[int, Field(default=0, gt=0)]

    @classmethod
    def from_ueye_rect(cls, rect: ueye.IS_RECT) -> "Rect":
        return cls(
            x=rect.s32X.value,
            y=rect.s32Y.value,
            width=rect.s32Width.value,
            height=rect.s32Height.value,
        )

    def to_ueye_rect(self) -> ueye.IS_RECT:
        rect = ueye.IS_RECT()
        rect.s32X = ueye.int(self.x)
        rect.s32Y = ueye.int(self.y)
        rect.s32Width = ueye.int(self.width)
        rect.s32Height = ueye.int(self.height)
        return rect


class UEyeCamera(Thing):
    """A camera from IDS Imaging"""

    def get_aoi(self) -> Rect:
        """Get current AOI from camera as Rect object (with x, y, width, height)"""
        rect_aoi = ueye.IS_RECT()
        ret = ueye.is_AOI(
            self.handle,
            ueye.IS_AOI_IMAGE_GET_AOI,
            rect_aoi,
            ueye.sizeof(rect_aoi),
        )
        assert return_code_OK(self.handle, ret)
        return Rect.from_ueye_rect(rect_aoi)

    def set_aoi(self, value: Rect) -> None:
        """Set camera AOI. Specify as x,y,width,height or a tuple
        (x, y, width, height) or as Rect object."""
        rect_aoi = value.to_ueye_rect()

        ret = ueye.is_AOI(
            self.handle,
            ueye.IS_AOI_IMAGE_SET_AOI,
            rect_aoi,
            ueye.sizeof(rect_aoi),
        )
        assert return_code_OK(self.handle, ret)

    AOI = Property(
        fget=get_aoi,
        fset=set_aoi,
        model=Rect,
        doc="Area of interest within the image",
    )  # type: Rect


import ctypes
from picosdk.ps6000 import ps6000 as ps
from picosdk.functions import assert_pico_ok

trigger_schema = {
    "type": "object",
    "properties": {
        "enabled": {"type": "boolean"},
        "channel": {
            "type": "string",
            "enum": ["A", "B", "C", "D", "EXTERNAL", "AUX"],
            # include both external and aux for 5000 & 6000 series
            # let the device driver will check if the channel is valid for the series
        },
        "threshold": {"type": "number"},
        "adc": {"type": "boolean"},
        "direction": {
            "type": "string",
            "enum": [
                "above",
                "below",
                "rising",
                "falling",
                "rising_or_falling",
            ],
        },
        "delay": {"type": "integer"},
        "auto_trigger": {"type": "integer", "minimum": 0},
    },
    "description": "Trigger settings for a single channel of the picoscope",
}


class Picoscope(Thing):
    """A PC based Oscilloscope from Picotech"""

    trigger = Property(doc="Trigger settings", model=trigger_schema)  # type: dict

    @trigger.setter
    def set_trigger(self, value: dict) -> None:
        channel = value["channel"].upper()
        direction = value["direction"].upper()
        enabled = ctypes.c_int16(int(value["enabled"]))
        delay = ctypes.c_int32(value["delay"])
        direction = ps.PS6000_THRESHOLD_DIRECTION[f"PS6000_{direction}"]
        if channel in ["A", "B", "C", "D"]:
            channel = ps.PS6000_CHANNEL["PS6000_CHANNEL_{}".format(channel)]
        else:
            channel = ps.PS6000_CHANNEL["PS6000_TRIGGER_AUX"]
        if not value["adc"]:
            if channel in ["A", "B", "C", "D"]:
                threshold = int(
                    threshold
                    * self.max_adc
                    * 1e3
                    / self.ranges[self.channel_settings[channel]["v_range"]]
                )
            else:
                threshold = int(self.max_adc / 5)
        threshold = ctypes.c_int16(threshold)
        auto_trigger = ctypes.c_int16(int(auto_trigger))
        self._status["trigger"] = ps.ps6000SetSimpleTrigger(
            self._ct_handle,
            enabled,
            channel,
            threshold,
            direction,
            delay,
            auto_trigger,
        )
        assert_pico_ok(self._status["trigger"])
