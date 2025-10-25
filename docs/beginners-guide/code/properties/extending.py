import typing, numpy, imageio
from hololinked.core import Property, Thing
from hololinked.param.parameterized import instance_descriptor


class JPEG(Property):
    """JPEG image data"""

    def __init__(
        self,
        default: Optional[numpy.ndarray] = None,
        compression_ratio: int = 1,
        transpose: bool = False,
        flip_horizontal: bool = False,
        flip_vertical: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(default=default, allow_None=True, **kwargs)
        if (
            not isinstance(compression_ratio, int)
            or not 0 <= compression_ratio <= 9
        ):
            raise ValueError("compression_ratio must be an integer from 0 to 9")
        self.compression_ratio = compression_ratio
        self.transpose = transpose
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical

    def validate_and_adapt(self, value) -> bytes:
        if value is None and not self.allow_None:
            # no need to check readonly & constant
            raise ValueError("image attribute cannot take None")
        if isinstance(value, bytes):
            raise ValueError(
                "Supply numpy.ndarray instead of pre-encoded JPEG image"
            )
        if isinstance(value, numpy.ndarray):
            if self.flip_horizontal:
                value = numpy.fliplr(value)
            if self.flip_vertical:
                value = numpy.flipud(value)
            if self.transpose:
                value = numpy.transpose(value)
            return imageio.imwrite(
                "<bytes>",
                value,
                format="JPEG",
                compress_level=self.compression_ratio,
            )
        raise ValueError(f"invalid type for JPEG image data - {type(value)}")

    @instance_descriptor
    def __set__(self, obj, value) -> None:
        if self.readonly:
            raise AttributeError("Cannot set read-only image attribute")
        if value is None and not self.allow_None:
            raise ValueError("None is not allowed")
        if isinstance(value, bytes):
            raise ValueError(
                "Supply numpy.ndarray instead of pre-encoded JPEG image"
            )
        if isinstance(value, numpy.ndarray):
            if self.flip_horizontal:
                value = numpy.fliplr(value)
            if self.flip_vertical:
                value = numpy.flipud(value)
            if self.transpose:
                value = numpy.transpose(value)
            binary = (
                imageio.imwrite(
                    "<bytes>",
                    value,
                    format="JPEG",
                    compress_level=self.compression_ratio,
                ),
            )
            return super().__set__(obj, binary)
        raise ValueError(f"invalid type for JPEG image data - {type(value)}")


class Camera(Thing):
    """Example object with custom defined JPEG property"""

    _image = JPEG(
        doc="Image data in JPEG format, not exposed to client, used internally",
        compression_ratio=2,
        transpose=False,
        flip_horizontal=True,
        remote=False,
    )  # type: bytes

    image = JPEG(
        readonly=True,  # dont allow clients to manipulate camera's image
        doc="latest captured image data in JPEG format",
        fget=lambda self: self._image,
    )  # type: bytes

    def capture(self):
        while True:
            image = self._capture_image()  # write image capture logic here
            self._image = image  # captured image

    horizontally_flipped_image = JPEG(
        doc="Image data in JPEG format, flipped horizontally",
        flip_horizontal=True,
    )  # type: bytes

    vertically_flipped_image = JPEG(
        doc="Image data in JPEG format, flipped vertically", flip_vertical=True
    )  # type: bytes

    transposed_image = JPEG(
        doc="Image data in JPEG format, transposed",
        flip_horizontal=False,
        flip_vertical=False,
        transpose=True,
    )  # type: bytes


class JPEG(Property):
    """JPEG image data"""

    __slots__ = [
        "compression_ratio",
        "transpose",
        "flip_horizontal",
        "flip_vertical",
    ]

    def __init__(
        self,
        default=None,
        compression_ratio: int = 1,
        transpose: bool = False,
        flip_horizontal: bool = False,
        flip_vertical: bool = False,
        **kwargs,
    ) -> None:
        # ... super().__init__ ...
        self.compression_ratio = compression_ratio
        self.transpose = transpose
        self.flip_horizontal = flip_horizontal
        self.flip_vertical = flip_vertical
