from enum import IntEnum
from pyueye import ueye
from hololinked.server import Thing, Property
from hololinked.server.properties import Integer, Number


class ErrorCodes(IntEnum):
    IS_NO_SUCCESS = -1
    IS_SUCCESS = 0
    IS_INVALID_CAMERA_HANDLE = 1
    IS_CANT_OPEN_DEVICE = 3
    IS_CANT_CLOSE_DEVICE = 4

    @classmethod
    def json(cls):
        # code to code name - opposite of enum definition
        return {
            value.value : name for name, value in vars(cls).items() if isinstance(
                                                                    value, cls)}
    

class IDSCamera(Thing):
    """Camera example object"""

    frame_rate = Number(default=1, bounds=(0, 40),
                        doc="frame rate of the camera", crop_to_bounds=True)

    @frame_rate.setter 
    def set_frame_rate(self, value):
        setFPS = ueye.double()
        ret = ueye.is_SetFrameRate(self.device, value, setFPS)
        if ret != ueye.IS_SUCCESS:
            raise Exception("could not set frame rate")
    
    @frame_rate.getter 
    def get_frame_rate(self) -> float:
        getFPS = ueye.double()
        ret = ueye.is_SetFrameRate(self.device, ueye.IS_GET_FRAMERATE, getFPS)
        if ret != ueye.IS_SUCCESS:
            raise Exception("could not get frame rate")
        return getFPS.value
    
    frame_rate = Number(default=1, bounds=(0, 40), crop_to_bounds=True,
      doc="frame rate of the camera", fget=get_frame_rate, fset=set_frame_rate)

    id = Integer(default=1, allow_None=True, bounds=(1, 255), 
                doc="Camera ID shown in IDS Camera Manager (not dev. ID)")

    # ------------------- class member example --------------------

    def error_codes_misplaced_getter(self):
        return {"info" : "this getter is never called"}
    
    error_codes = Property(readonly=True, default=ErrorCodes.json(), 
                        class_member=True, doc="error codes raised by IDS library",
                        fget=error_codes_misplaced_getter)    
    
    # ------------------- state machine example --------------------
    
    def get_pixelclock(self) -> int:
        cint_in = ueye.uint()
        ret = ueye.is_PixelClock(self.handle, ueye.IS_PIXELCLOCK_CMD_GET,
                                    cint_in, ueye.sizeof(cint_in))
        assert return_code_OK(self.handle, ret)
        return cint_in.value
    
    def set_pixelclock(self, value : int) -> None:
        cint_in = ueye.uint(value)
        ret = ueye.is_PixelClock(self.handle, ueye.IS_PIXELCLOCK_CMD_SET,
                                    cint_in, ueye.sizeof(cint_in))
        assert return_code_OK(self.handle, ret)
            
    pixel_clock = Integer(doc="Pixel clock in MHz", bounds=(0, None), state=["ON"], 
                    metadata=dict(unit='MHz'), inclusive_bounds=(False, True),
                    fget=get_pixelclock, fset=set_pixelclock) # type: int
    
    # ------------------- observable example --------------------

    def set_exposure(self, value : float) -> None:
        cdbl_in = ueye.double(value)
        ret = ueye.is_Exposure(self.handle, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, 
                            cdbl_in, ueye.sizeof(cdbl_in))
        assert return_code_OK(self.handle, ret)

    def get_exposure(self) -> float:
        cdbl_out = ueye.double()
        ret = ueye.is_Exposure(self.handle, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, 
                            cdbl_out, ueye.sizeof(cdbl_out))
        assert return_code_OK(self.handle, ret)
        return cdbl_out.value

    exposure_time = Number(bounds=(0, None), inclusive_bounds=(False, True), 
                        doc="Exposure time for image in milliseconds",
                        observable=True, metadata=dict(unit='ms'),
                        fget=get_exposure, fset=set_exposure) # type: float
    
    
if __name__ == '__main__':
    cam = IDSCamera(id='camera')
    print(cam.id) # prints 1
    print(cam.frame_rate) # does not print default, 
    # but the actual value in device after invoking the getter
    print("error codes class level", IDSCamera.error_codes) # prints error codes
    print("error codes instance level", cam.error_codes) # prints error codes
    print(IDSCamera.error_codes == cam.error_codes) # prints True

     

  


