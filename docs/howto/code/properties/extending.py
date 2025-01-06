import typing, numpy, imageio
from hololinked.server import Property
from hololinked.param.parameterized import instance_descriptor

class JPEG(Property):
    """JPEG image data"""
    
    def __init__(self, default = None, 
                compression_ratio : int = 1, transpose : bool = False, 
                flip_horizontal : bool = False, flip_vertical : bool = False,
                **kwargs,
            ) -> None:
        super().__init__(default=default, allow_None=True, **kwargs)
        assert (isinstance(compression_ratio, int) and 
            compression_ratio >= 0 and compression_ratio <= 9
            ), "compression_ratio must be an integer between 0 and 9"
        self.compression_ratio = compression_ratio
        self.transpose = transpose
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical
    
    def validate_and_adapt(self, value) -> typing.Any:
        if value is None and not self.allow_None:
            # no need to check readonly & constant 
            raise ValueError("image attribute cannot take None")
        if isinstance(value, bytes):
            raise ValueError("Supply numpy.ndarray instead of pre-encoded JPEG image")
        if isinstance(value, numpy.ndarray):
            if self.flip_horizontal:
                value = numpy.fliplr(value)
            if self.flip_vertical:
                value = numpy.flipud(value)
            if self.transpose:
                value = numpy.transpose(value)
            return imageio.imwrite('<bytes>', value, format='JPEG', 
                                compress_level=self.compression_ratio)
        raise ValueError(f"invalid type for JPEG image data - {type(value)}")
    
    @instance_descriptor
    def __set__(self, obj, value) -> None:
        if self.readonly:
            raise AttributeError("Cannot set read-only image attribute")
        if value is None and not self.allow_None:
            raise ValueError("None is not allowed")
        if isinstance(value, bytes):
            raise ValueError("Supply numpy.ndarray instead of pre-encoded JPEG image")
        if isinstance(value, numpy.ndarray):
            if self.flip_horizontal:
                value = numpy.fliplr(value)
            if self.flip_vertical:
                value = numpy.flipud(value)
            if self.transpose:
                value = numpy.transpose(value)
            return super().__set__(obj, 
                                imageio.imwrite('<bytes>', value, format='JPEG', 
                                    compress_level=self.compression_ratio)
                            )        
        raise ValueError(f"invalid type for JPEG image data - {type(value)}")
    


from hololinked.server import Thing

class Camera(Thing):
   
    _image = JPEG(doc="Image data in JPEG format", 
                compression_ratio=2, transpose=False, 
                flip_horizontal=True, remote=False) # type: bytes
    
    image = JPEG(readonly=True, doc="Image data in JPEG format",
                fget=lambda self: self._image) # type: bytes
    
    def capture(self):
        while True:
            # write image capture logic here
            self._image = image # captured image

    horizontally_flipped_image = JPEG(doc="Image data in JPEG format",
                                    flip_horizontal=True) # type: bytes

    vertically_flipped_image = JPEG(doc="Image data in JPEG format", 
                                flip_vertical=True) # type: bytes
    
    transposed_image = JPEG(doc="Image data in JPEG format", 
                            flip_horizontal=False, flip_vertical=False,
                            transpose=True) # type: bytes
    


class JPEG(Property):
    """JPEG image data"""
    
    __slots__ = ['compression_ratio', 'transpose', 'flip_horizontal', 'flip_vertical']

    def __init__(self, default = None, 
                compression_ratio : int = 1, transpose : bool = False, 
                flip_horizontal : bool = False, flip_vertical : bool = False,
                **kwargs,
            ) -> None:
        # ... super().__init__ ...
        self.compression_ratio = compression_ratio
        self.transpose = transpose
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical