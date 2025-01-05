# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 17:25:57 2020

@author: Felix.Balling
"""
import ctypes
import numpy as np
import traceback
import typing

from picosdk.ps6000 import ps6000 as ps
from picosdk.functions import assert_pico_ok

from hololinked.server.properties import List, Integer 
from hololinked.server import action

from .base import Picoscope



analog_offset_input_schema = {
    'type': 'object',
    'properties' : {
        'voltage_range' : { 
            'type': 'string',
            'enum': ['10mV', '20mV', '50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V',
                            '10V', '20V', '50V', 'MAX_RANGES'] 
        },
        'coupling' : { 
            'type': 'string', 
            'enum': ['AC', 'DC'] 
        }
    }
}


analog_offset_output_schema = {
    'type': 'array',
    'minItems': 2,
    'items' : {
        'type': 'number',
    }
}


set_channel_schema = {
    'type': 'object',
    'properties' : {
        'channel' : { 
            'type': 'string', 
            'enum': ['A', 'B', 'C', 'D'] 
        },
        'enabled' : { 
            'type': 'boolean' 
        },
        'voltage_range' : { 
            'type': 'string', 
            'enum': ['10mV', '20mV', '50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V', 
                '10V', '20V', '50V', 'MAX_RANGES'] 
        },
        'offset' : { 
            'type': 'number' 
        },
        'coupling' : { 
            'type': 'string', 
            'enum': ['AC', 'DC'] 
        },
        'bw_limiter' : { 
            'type': 'string', 
            'enum': ['full', '20MHz'] 
        }
    }
}



class Picoscope6000(Picoscope):
    """
    6000 series picoscopes using 6000 driver from picosdk.
    For manual, see:
    https://www.picotech.com/download/manuals/picoscope-6000-series-a-api-programmers-guide.pdf
    """

    max_adc = Integer(doc='max value of the ADC possible for given resolution of data, 32512 for 8 bits & 32767 for higher bits.', 
                    readonly=True, default=32512) # type: int


    @action(input_schema=connect_schema)
    def connect(self, serial_number : typing.Optional[str] = None) -> None:
        """
        Open a Picoscope 6000. Serial number is mandatory and does not open first
        available device. 

        Parameters
        ----------
        serial_number : str, optional
            Serial number of the scope to be opened (looks like 'CR524/015').

        Returns
        -------
        None.

        """
        if serial_number:
            self.serial_number = serial_number
        else:
            serial_number = self.serial_number
        sb = ctypes.create_string_buffer(10)
        sb.value = bytes(serial_number, encoding='utf-8')
        self._status['open-unit'] = ps.ps6000OpenUnit(ctypes.byref(self._ct_handle), sb)
        assert_pico_ok(self._status['open-unit'])
        for code in range(11):
            self.get_unit_info(code)
        self.mode = self._info[3]


    @action()
    def disconnect(self) -> None:
        """
        Close the unit.

        Returns
        -------
        None.

        """
        self.stop_acquisition()
        self._status['close-unit'] = ps.ps6000CloseUnit(self._ct_handle)
        assert_pico_ok(self._status['close-unit'])


    @action(input_schema=get_unit_info_schema)
    def get_unit_info(self, info_code : int) -> str:
        """
        Get information about the opened unit.

        Parameters
        ----------
        info : int
            Code for the required information (for values see below).

        Returns
        -------
        string : str
            The returned information.

        Info Codes
        ----------
        0: PICO_DRIVER_VERSION
            Version number of the DLL
        1: PICO_USB_VERSION
            Type of USB connection
        2: PICO_HARDWARE_VERSION
            Hardware version of the device
        3: PICO_VARIANT_INFO
            Model number
        4: PICO_BATCH_AND_SERIAL
            Serial number of the scope
        5: PICO_CAL_DATE
            Calibration date
        6: PICO_KERNEL_VERSION
            Version of the kernel driver
        7: PICO_DIGITAL_HARDWARE_VERSION
            Hardware version of the digital section
        8: PICO_ANALOG_HARDWARE_VERSION
            Hardware version of the analog section
        9: PICO_FIRMWARE_VERSION_1
            Version of firmware 1
        A: PICO_FIRMWARE_VERSION_2
            Version of firmware 2
        """
        length = ctypes.c_int16(10)
        string = ctypes.create_string_buffer(length.value)
        req_size = ctypes.create_string_buffer(length.value)
        info = ctypes.c_uint32(info_code)
        self._status['unit-info'] = ps.ps6000GetUnitInfo(self._ct_handle, string,
                                                        length, req_size, info)
        assert_pico_ok(self._status['unit-info'])
        self._info[info_code] = string.value 
        return string.value
    
    
    ranges = List(default=[10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 
                        20000, 50000, 100000, 200000], readonly=True, 
                        doc="Voltage ranges supported by picoscope in mV unit")
   
    @action(input_schema=set_channel_schema)
    def set_channel(self, 
                channel: str, enabled: bool = True, 
                v_range: str ='2V', offset: float = 0, 
                coupling: str = 'DC_1M', bw_limiter: str = 'full'
            ) -> None:
        """
        Set the parameter for a channel.
        https://www.picotech.com/download/manuals/picoscope-6000-series-a-api-programmers-guide.pdf
       
        Parameters
        ----------
        channel : {'A', 'B', 'C', 'D'}
            Channel to set.
        enabled : `bool`, optional
            Enable or disable the channel. The default is True.
        v_range : {'50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V', '10V', '20V', '50V', 'MAX_RANGES'}, optional
            Voltage range of the channel. The default is '2V'.
        offset : float, optional
            Analog offset of the channel. The range of offsets depends on the
            selected voltage range. For details see Programmers Guide.
            The default is 0.
        coupling : {'AC', 'DC_1M', 'DC_50R'}, optional
            Coupling of the channel. For 50Ohm impedance the 20V and 50V ranges
            are not available. AC coupling implies 1MOhm impedance and is only
            sensitive for frequencies higher than 1 hertz.
            The default is 'DC_1M'.
        bw_limiter : {'full', '20MHz'}, optional
            Bandwidth limiter (-3dB limit). The default is 'full'.

            
        """
        ch = ps.PS6000_CHANNEL['PS6000_CHANNEL_{}'.format(channel.upper())]
        enabled = ctypes.c_int16(enabled)
        _vmax, _vmin = self.get_analogue_offset(v_range, coupling)
        if offset > _vmax or offset < _vmin:
            raise ValueError(
                'Invalid Offset {}\nOffset has to be between {} and {}'.format(
                    offset, _vmin, _vmax))
        offset = ctypes.c_float(offset)
        coupling = ps.PS6000_COUPLING['PS6000_{}'.format(coupling.upper())]
        v_range = ps.PS6000_RANGE['PS6000_{}'.format(v_range.upper())]
        bw_limiter = ps.PS6000_BANDWIDTH_LIMITER['PS6000_BW_{}'.format(
            bw_limiter.upper())]
        self._status['set-channel-{}'.format(channel)] = ps.ps6000SetChannel(
                                        self._ct_handle, ch, enabled, coupling,
                                        v_range, offset, bw_limiter
                                    )
        assert_pico_ok(self._status['set-channel-{}'.format(channel)])
        self.channel_settings[channel].update({
                                    'enabled': enabled.value, 'v_range': v_range,
                                    'offset': offset.value, 'coupling': coupling,
                                    'bw_limiter': bw_limiter
                                })
        
    @action(input_schema=set_trigger_schema)
    def set_trigger(self, channel : str, enabled : bool, threshold : float, adc : bool = False,
                    direction : str = 'rising', delay : int = 0, auto_trigger : int = 1000) -> None:
        """
        Set a trigger using the simplified `ps6000SetSimpleTrigger` function.

        Parameters
        ----------
        enabled : `bool`
            Arm or disable the trigger.
        channel : {'A', 'B', 'C', 'D', 'AUX'}
            Source of the trigger. Can be any channel or the AUX input.
        threshold : `float`
            Threshold of the trigger. Depending on the value of `adc` given in
            [V] or ADC counts. By default in [V]. Note that the trigger has to
            be reset, if the voltage range of the trigger channel is changed.
        adc : `bool`, optional
            If True the threshold is given in ADC counts, if False as voltage.
            The default is False.
        direction : {'above', 'below', 'rising', 'falling', 'rising_or_falling'}, optional
            Direction for the trigger. The default is 'rising'.
        delay : int, optional
            The delay between the trigger and the first sample taken in [s].
            The default is 0.
        auto_trigger (or auto trigger time): int
            Time in [ms] the device will wait if no trigger occurs. Use 0 for
            waiting indefinitely.

        Returns
        -------
        None.

        Voltage to ADC conversion
        -------------------------
        The scope scales the samples to 16 bits. The max and min values are
        stored in constants: PS6000_MAX_VALUE (32512) and PS6000_MIN_VALUE
        (-32512). For conversion between voltage U and ADC the selected voltage
        range U_max has to be taken into account:
            ADC = U * 32512 / U_max
        """
        enabled = ctypes.c_int16(int(enabled))
        direction = ps.PS6000_THRESHOLD_DIRECTION['PS6000_{}'.format(
                                                  direction.upper())]
        ch = channel.upper()
        if channel.upper() in ['A', 'B', 'C', 'D']:
            channel = ps.PS6000_CHANNEL['PS6000_CHANNEL_{}'.format(
                                        channel.upper())]
        else:
            channel = ps.PS6000_CHANNEL['PS6000_TRIGGER_AUX']
        if not adc:
            if channel in ['A', 'B', 'C', 'D']:
                threshold = int(threshold * self.max_adc * 1e3
                            / self.ranges[self.channel_settings[ch]['v_range']])
                # print(threshold)
            else:
                threshold = int(self.max_adc/5)
        threshold = ctypes.c_int16(threshold)
        auto_trigger = ctypes.c_int16(int(auto_trigger))
        self._status['trigger'] = ps.ps6000SetSimpleTrigger(self._ct_handle,
                                    enabled, channel, threshold, direction, 
                                    delay, auto_trigger)
        assert_pico_ok(self._status['trigger'])


    @action(
        input_schema=analog_offset_input_schema, 
        output_schema=analog_offset_output_schema
    )
    def get_analogue_offset(self, 
                    voltage_range : str, 
                    coupling : str
                ) -> typing.Tuple[float, float]:
        v_max = ctypes.c_float()
        v_min = ctypes.c_float()
        v_range = ps.PS6000_RANGE['PS6000_{}'.format(voltage_range.upper())]
        coupling = ps.PS6000_COUPLING['PS6000_{}'.format(coupling.upper())]
        self._status['getAnalogueOffset'] = ps.ps6000GetAnalogueOffset(
                                self._ct_handle, v_range, coupling, 
                                ctypes.byref(v_max), ctypes.byref(v_min))
        assert_pico_ok(self._status['getAnalogueOffset'])
        return v_max.value, v_min.value

    
    @action(input_schema=get_timebase_schema, output_schema=get_timebase_output_schema) 
    def get_timebase(self, interval : float = 1000, resolution : float = 8, oversample : int = 0):
        """
        Get timebase and sampling parameters from the scope.

        Parameters
        ----------
        interval : `float`
            Requested time interval in [us].
        resolution : `float`
            Requested time sampling in [ns].
        oversample : int, optional
            Required oversampling. Has to be between 0 and
            `PS6000_MAX_OVERSAMPLE_8BIT`. The default is 0.

        Returns
        -------
        tb: int
            Integer encoding the timebase. For explanation see Programmers
            Guide.
        dtns: `float`
            Actual sampling interval for this timebase and settings.
        max_samples: int
            Max number of samples available with these settings.
        max_interval : `float`
            Max time interval in this timebase in [us].
        """
        no_samples = int(interval / resolution * 1e3)
        if resolution < 4:
            tb = int(np.log2(resolution * 5))
        else:
            tb = int(resolution * 0.15625 + 4)
        dtns = ctypes.c_float()
        max_samples = ctypes.c_uint32()
        self._status['get-timebase'] = ps.ps6000GetTimebase2(self._ct_handle, tb,
           no_samples, ctypes.byref(dtns), oversample, ctypes.byref(max_samples), 0)
        assert_pico_ok(self._status['get-timebase'])
        max_interval = dtns.value * max_samples.value / 1e3
        return tb, dtns.value, max_samples.value, max_interval

    @action()
    def run_block(self, pre_trigger_samples : int, post_trigger_samples : int, timebase : int,
                oversample : int = 0, seg_index : int = 0, lp_ready = None, p_param = None) -> float:
        """
        Run a block acquisition with the previously set channel settings.

        Parameters
        ----------
        pre_trigger_samples : int
            Number of samples to take before trigger.
        post_trigger_samples : int
            Number of samples to take after trigger.
        timebase : int
            Timebase as returned by `get_timebase`.
        oversample : int, optional
            Oversampling factor (max 256). The default is 0.
        seg_index : int, optional
            Index specifying which memory segment to use. The default is 0.
        lp_ready : `function pointer`, optional
            Pointer to the callback function which is called when the data has
            been collected. If None the default `ps6000IsReady` is used.
            The default is None.
        p_param : `void pointer`, optional
            Pointer passed to the callback function. The default is None.

        Returns
        -------
        time_indisposed : int
            Time the scope will spend collection samples in [ms].

        """
        time_indisposed = ctypes.c_int32()
        self._status['run-block'] = ps.ps6000RunBlock(self._ct_handle,
            pre_trigger_samples, post_trigger_samples, timebase, oversample,
            ctypes.byref(time_indisposed), seg_index, lp_ready, p_param)
        assert_pico_ok(self._status['run-block'])
        return time_indisposed.value


    def check_ready(self):
        """
        Perform a single check if the scope has finished data acquisition using
        the default callback.

        Returns
        -------
        ready : `bool`
            Return value of the callback, indicating if the scope is ready.

        """
        ready = ctypes.c_int16(0)
        self._status['is-ready'] = ps.ps6000IsReady(self._ct_handle,
                                                   ctypes.byref(ready))
        return bool(ready.value)


    def wait_ready(self):
        """
        Wait for the scope to finish data acquisition.

        WARNING : No timeout implemented
        """
        ready = False
        while ready == False:
            ready = self.check_ready()


    @action(input_schema=set_data_buffer_schema)
    def set_data_buffer(self, channel : str, num_samples : int, 
                    downsample_ratio_mode : int = ps.PS6000_RATIO_MODE['PS6000_RATIO_MODE_NONE']):
        """
        Prepare a data buffer for a single channel.

        Parameters
        ----------
        channel : {'A', 'B', 'C', 'D'}
            Channel name.
        num_samples : int
            Size of the buffer.
        downsample_ratio_mode : int, optional
            Mode to use for downsampling. The default is 0.

        Returns
        -------
        buffer : `c_short_array`
            Empty array in which the data will be written.

        """
        ch = ps.PS6000_CHANNEL['PS6000_CHANNEL_{}'.format(channel.upper())]
        buffer = (ctypes.c_int16 * num_samples)()
        self._status['set-data-buffer-{}'.format(channel)] = ps.ps6000SetDataBuffer(
            self._ct_handle, ch, ctypes.byref(buffer), num_samples,
            downsample_ratio_mode)
        assert_pico_ok(self._status['set-data-buffer-{}'.format(channel)])
        return buffer


    @action()
    def get_values(self, num_samples : int, start_index : int = 0, downsample_ratio : int = 1,
                   downsample_mode : int = ps.PS6000_RATIO_MODE['PS6000_RATIO_MODE_NONE'], 
                   seg_index : int = 0):
        """
        Retrieve the data from the scope to previously set buffers (see
        `set_data_buffer`).

        Parameters
        ----------
        num_samples : int
            Number of samples requested.
        start_index : int, optional
            Index indicating the start point for data collection.
            The default is 0.
        downsample_ratio : int, optional
            Downsampling factor applied to the raw data. Has to be greater
            than 0. The default is 1.
        downsample_mode : int, optional
            Index indicating the downsampling mode applied. 0 corresponds to
            no downsampling. The default is 0.
        seg_index : int, optional
            Number of the memory segment the data is stored in.
            The default is 0.

        Returns
        -------
        num_samples : int
            Actual number of samples retrieved from the scope.
        overflow : int
            Bitmask indicating overvoltages for each channel. Bit 0 corresponds
            to channel 'A'.

        """
        cnum_samples = ctypes.c_int32(num_samples)
        overflow = ctypes.c_int16()
        self._status['get_values'] = ps.ps6000GetValues(self._ct_handle,
           start_index, ctypes.byref(cnum_samples), downsample_ratio,
           downsample_mode, seg_index, ctypes.byref(overflow))
        assert_pico_ok(self._status['get_values'])
        return cnum_samples.value, overflow.value

   

if __name__ == '__main__':
    adcmax = 32512
    pico = Picoscope6000()
    # pico.open_unit(b'015')
    pico.open_unit()
    print(pico.status)
    try:
        pico.set_channel('A', v_range='5V', coupling='DC_1M', offset=-4.0)
        pico.set_channel('B', v_range='5V', coupling='DC_1M', offset=-4.0)
        pico.set_channel('C', v_range='5V', coupling='DC_1M', offset=0.0)
        print(pico.settings)
        thres = int(1.5/5*adcmax)
        props = [{'thresholdUpper': int(-3.8/5*adcmax), 'channel': 'A'},
                 {'thresholdUpper': int(1.0/5*adcmax), 'channel': 'C'}]
        dirs = {'A': 'rising', 'C': 'above'}
        cons = [{'A': 'true', 'B': 'dont_care', 'C': 'dont_care'}]
        pico.set_trigger_channel_conditions(cons)
        pico.set_trigger_channel_directions(dirs)
        pico.set_trigger_channel_properties(props, 0)
        pico.set_trigger_delay(0)
        # pico.set_trigger(True, 'C', -2.8, False, 'rising', 0, 10000)
        # bs = pico.run_block_hl(10000, 1000, 1000)
        # pico.start_acquisition(2, 1, 0)
    except Exception:
        traceback.print_exc()
    finally:
        pico.close_unit()