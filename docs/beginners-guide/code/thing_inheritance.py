from hololinked.core import Thing, Property, action, Event


class OceanOpticsSpectrometer(Thing):
    """
    add class doc here
    """

    def __init__(self, id, serial_number, autoconnect, **kwargs):
        super().__init__(id=id, **kwargs)
        self.serial_number = serial_number
        if autoconnect:
            self.connect()

    def connect(self):
        """
        implement device driver logic/hardware communication protocol here
        to connect to the hardware
        """
        pass
