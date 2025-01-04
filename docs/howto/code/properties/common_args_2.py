from enum import IntEnum
from pyueye import ueye
from hololinked.server import Thing, Property
from hololinked.server.properties import Integer, Number

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
    
    # same as
    # frame_rate = Number(default=1, bounds=(0, 40), crop_to_bounds=True,
    #   doc="frame rate of the camera", fget=get_frame_rate, fset=set_frame_rate)

    id = Integer(default=1, allow_None=True, bounds=(1, 255), 
                doc="Camera ID shown in IDS Camera Manager (not dev. ID)")
 
if __name__ == '__main__':
    cam = IDSCamera(id='camera')
    print(cam.id) # prints 1
    print(cam.frame_rate) # does not print default, 
    # but the actual value in device after invoking the getter
    

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

    def error_codes_misplaced_getter(self):
        return {"info" : "this getter is never called"}
    
    error_codes = Property(readonly=True, default=ErrorCodes.json(), 
                        class_member=True, doc="error codes raised by IDS library",
                        fget=error_codes_misplaced_getter)    
    
if __name__ == '__main__':
    cam = IDSCamera(id='camera')
    print("error codes class level", IDSCamera.error_codes) # prints error codes
    print("error codes instance level", cam.error_codes) # prints error codes
    print(IDSCamera.error_codes == cam.error_codes) # prints True


