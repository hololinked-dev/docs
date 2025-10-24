from hololinked.core import Thing
from hololinked.core.properties import String, Number, Selector, Boolean, List


class OceanOpticsSpectrometer(Thing):
    """
    Spectrometer example object
    """

    serial_number = String(
        default="USB2+H15897",
        allow_None=False,
        doc="serial number of the spectrometer",
    )  # type: str

    def __init__(
        self, id: str, serial_number: str, integration_time: float
    ) -> None:
        super().__init__(id=id, serial_number=serial_number)
        self.connect()  # connect first before setting integration time
        self.integration_time = integration_time

    integration_time = Number(
        default=1000,
        bounds=(0.001, None),
        crop_to_bounds=True,
        doc="integration time of measurement in millisec",
    )  # type: int

    @integration_time.setter
    def set_integration_time(self, value):
        # value is already validated as a float or int
        # & cropped to specified bounds when this setter invoked
        self.device.integration_time_micros(int(value * 1000))

    @integration_time.getter
    def get_integration_time(self):
        return self.device.read_integration_time_micros() / 1000
        # NOTE - seabreeze dont offer a read_integration_time_micros() method, this is an example

    nonlinearity_correction = Boolean(
        default=False,
        doc="""set True for auto CCD nonlinearity correction. 
            Not supported by all models, like STS.""",
    )  # type: bool

    trigger_mode = Selector(
        objects=[0, 1, 2, 3, 4],
        default=0,
        doc="""0 = normal/free running, 
            1 = Software trigger, 2 = Ext. Trigger Level,
            3 = Ext. Trigger Synchro/ Shutter mode,
            4 = Ext. Trigger Edge""",
    )  # type: int

    @trigger_mode.setter
    def apply_trigger_mode(self, value: int):
        self.device.trigger_mode(value)

    @trigger_mode.getter
    def get_trigger_mode(self):
        return self.device.read_trigger_mode()
        # NOTE - seabreeze dont offer a read_trigger_mode() method, this is an example

    intensity = List(
        default=None,
        allow_None=True,
        doc="captured intensity",
        readonly=True,
        fget=lambda self: self._intensity.tolist(),
    )
