import multiprocessing, os, ssl, threading, logging
from hololinked.core import Thing, Property, action, Event
from hololinked.core.properties import Number, Selector, String, List
from hololinked.server import HTTPServer
from seabreeze.spectrometers import Spectrometer


class OceanOpticsSpectrometer(Thing):
    """
    Spectrometer example object
    """

    serial_number = String(
        default=None, allow_None=True, doc="serial number of the spectrometer"
    )  # type: str

    def __init__(self, id, serial_number, autoconnect, **kwargs):
        super().__init__(id=id, serial_number=serial_number, **kwargs)
        # you can also pass properties to init to auto-set (optional)
        if autoconnect and self.serial_number is not None:
            self.connect(trigger_mode=0, integration_time=int(1e6))
            # let's say, by default
        self._acquisition_thread = None

    @action()
    def connect(self, trigger_mode, integration_time):
        self.device = Spectrometer.from_serial_number(self.serial_number)
        if trigger_mode:
            self.device.trigger_mode(trigger_mode)
        if integration_time:
            self.device.integration_time_micros(integration_time)

    @action()
    def disconnect(self):
        self.device.close()

    integration_time = Number(
        default=1000,
        bounds=(0.001, 1e6),
        doc="""integration time of measurement in milliseconds,
                        1μs (min) or 1s (max)""",
        crop_to_bounds=True,
    )

    @integration_time.setter
    def set_integration_time(self, value: float):
        self.device.integration_time_micros(int(value * 1000))
        self._integration_time = int(value)

    @integration_time.getter
    def get_integration_time(self) -> float:
        try:
            return self._integration_time
        except AttributeError:
            return 1000.0

    trigger_mode = Selector(
        objects=[0, 1, 2, 3, 4],
        default=0,
        doc="""0 = normal/free running, 1 = Software trigger, 2 = Ext. Trigger Level,
                        3 = Ext. Trigger Synchro/ Shutter mode, 4 = Ext. Trigger Edge""",
    )

    @trigger_mode.setter
    def set_trigger_mode(self, value: int):
        self.device.trigger_mode(value)
        self._trigger_mode = value

    @trigger_mode.getter
    def get_trigger_mode(self):
        try:
            return self._trigger_mode
        except:
            return self.parameters["trigger_mode"].default

    intensity = List(
        default=None,
        allow_None=True,
        doc="captured intensity",
        readonly=True,
        fget=lambda self: self._intensity.tolist(),
    )

    measurement_event = Event(
        name="intensity-measurement-event",
        doc="""event generated on measurement of intensity, 
            max 30 per second even if measurement is faster.""",
    )

    def capture(self):
        self._run = True
        while self._run:
            self._intensity = self.device.intensities(
                correct_dark_counts=False, correct_nonlinearity=False
            )
            self.measurement_event.push(self._intensity.tolist())
            self.logger.debug(f"pushed measurement event")

    @action()
    def start_acquisition(self):
        if self._acquisition_thread is None:  # _acquisition_thread defined in __init__
            self._acquisition_thread = threading.Thread(target=self.capture)
            self._acquisition_thread.start()

    @action()
    def stop_acquisition(self):
        if self._acquisition_thread is not None:
            self.logger.debug(f"""stopping acquisition thread with 
                            thread-ID {self._acquisition_thread.ident}""")
            self._run = False  # break infinite loop
            self._acquisition_thread.join()
            self._acquisition_thread = None


def start_https_server():
    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(
        f"assets{os.sep}security{os.sep}certificate.pem",
        keyfile=f"assets{os.sep}security{os.sep}key.pem",
    )
    # You need to create a certificate on your own or use without one
    # for quick-start but events will not be supported by browsers
    # if there is no SSL

    HTTPServer(
        ["spectrometer"], port=8083, ssl_context=ssl_context, log_level=logging.DEBUG
    ).listen()


if __name__ == "__main__":
    spectrometer = OceanOpticsSpectrometer(
        id="spectrometer",
        serial_number="S14155",
        autoconnect=True,
        log_level=logging.DEBUG,
    )
    spectrometer.run_with_http_server(port=3569)

    multiprocessing.Process(target=start_https_server).start()
    # Remove above line if HTTP not necessary. One can also thread the HTTP server.
    # threading.Thread(target=start_https_server).start()
    spectrometer = OceanOpticsSpectrometer(
        id="spectrometer", serial_number=None, autoconnect=False
    )
    spectrometer.run_with_zmq_server(access_points="IPC")
    # ZMQ interprocess-communication - suitable for beginners and
    # apps automatically behind firewall

    # example code, but will never reach here unless exit() is called by the client
    spectrometer = OceanOpticsSpectrometer(
        id="spectrometer",
        zmq_serializer="pickle",
        serial_number=None,
        autoconnect=False,
    )
    spectrometer.run(zmq_protocols=["TCP", "IPC"], tcp_socket_address="tcp://*:6539")

    # example code, but will never reach here unless exit() is called by the client
    spectrometer = OceanOpticsSpectrometer(
        id="spectrometer", serial_number=None, autoconnect=False
    )
    spectrometer.run(zmq_protocols="TCP", tcp_socket_address="tcp://*:6539")

    # example code, but will never reach here unless exit() is called by the client
    spectrometer = OceanOpticsSpectrometer(
        id="spectrometer",
        zmq_serializer="pickle",
        serial_number=None,
        autoconnect=False,
    )
    spectrometer.run(zmq_protocols=["TCP", "IPC"], tcp_socket_address="tcp://*:6539")


# Another example


class Axis(Thing):
    """
    Represents a single axis of stepper module controlling a linear stage
    """

    def execute(self, command):
        # implement device driver logic to send command to hardware
        ...

    referencing_run_frequency = Number(
        bounds=(0, 40000),
        inclusive_bounds=(False, True),
        step=100,
        doc="""Run frequency during initializing (referencing), in Hz (integer value).
            I1AM0x: 40 000 maximum, I4XM01: 4 000 000 maximum""",
    )

    @referencing_run_frequency.getter
    def get_referencing_run_frequency(self):
        resp = self.execute("P08R")
        return int(resp)

    @referencing_run_frequency.setter
    def set_referencing_run_frequency(self, value):
        self.execute("P08S{}".format(value))
