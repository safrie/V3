# -*- coding: utf-8 -*-
"""
Abstract base class for shared methods/attributes for Keithley measurements.

Classes_
    KeithMeasure

Part of the probe station V3 collection.
@author: Sarah Friedensen
"""
from abc import ABCMeta, abstractmethod


class KeithMeasure():
    """ABC for universal attributes/methods for Keithley IV measurements.

    attributes_
        curr1_text: What curr1 represents in labels/headers.
        curr2_text: What curr2 represents in labels/headers.
        curr_step_text: What curr_step represents in labels/headers.
        curr_delta_text: What curr_delta represents in labels/headers.
        meas_rate_text: What meas_rate represents in labels/headers.
        meas_delay_text: What meas_delay represents in labels/headers.
        pulse_width_text: What pulse_width represents in labels/headers.
        pulse_count_text: What pulse_count represents in labels/headers.
        unit_idx: Index for what unit measurement uses.
        curr1: Float for current1.
        curr2: Float for current2.
        num_points: Number of points for the measurement.
        meas_delay: How long 2182A will wait to measure after current change by
            6221 (units vary).
        low_meas: Whether or not 2nd 'low' measurement occurs (if applicable).
        filter_idx: Index specifying filter type.
        filter_type: String specifying filter type.
        filter_on: Whether or not filtering is enabled.
        filter_window: Filter window by % of measurement.  Range is 0-10.
        filter_count: Number of measurements to bin in order to filter.

    methods_
        __init__()
        get_meas_type_str()
        set_unit_idx(int)
        set_curr1(float)
        set_curr2(float)
        set_curr_step(float)
        set_curr_delta(float)
        set_num_points(int)
        calc_num_points(float, float, float)
        set_num_sweeps(int)
        set_meas_rate(int)
        set_meas_delay(float)
        set_pulse_width(float)
        set_pulse_count(int) MAYBE
        set_low_meas(bool)
        set_filter_idx(int)
        set_filter_on(bool)
        set_filter_window(int)
        set_filter_count(int)
        get_total_points()
        update_num_points()
    """

    __metaclass__ = ABCMeta
    curr1_text = ''
    curr2_text = ''
    curr_step_text = ''
    curr_delta_text = ''
    meas_rate_text = ''
    meas_delay_text = ''
    pulse_width_text = ''
    pulse_count_text = ''

    def __init__(self) -> None:
        """Instantiate general Keithley 6221/2182A transport measurement."""
        self.unit_idx = 0
        self.curr1 = 0
        self.curr2 = 0
        self.num_points = 0
        self.meas_delay = 2
        self.low_meas = True
#        self.filter_idx = 0
#        self.filter_type = 'Moving'
        self.filter_on = False
        self.filter_window = 0
        self.filter_count = 10
        self.pulse_width = None
#        self.num_sweeps = None

    @abstractmethod
    def get_meas_type_str(self) -> None:
        """Return a string of the type of measurement."""

    def set_unit_idx(self, idx: int) -> None:
        """Set the unit index for the Keithleys to idx."""
        self.unit_idx = idx

    def set_curr1(self, num: float) -> None:
        """Set curr1 to num."""
        self.curr1 = num

    def set_curr2(self, num: float) -> None:
        """Set curr2 to num."""
        self.curr2 = num

    def set_curr_step(self, num: float) -> None:
        """Overidden in daughter classes in which current step functions."""
        pass

    def set_curr_delta(self, num: float) -> None:
        """Overidden in daughter classes in which current delta functions."""
        pass

    def set_num_points(self, points: int) -> None:
        """Set the number of points for a measurement to points.

        Delta, pulse delta, and pulse delta log sweep measurements require the
        user to specify the number of points to measure.
        """
        self.num_points = points

    def calc_num_points(self, start: float, stop: float, step: float) -> int:
        """Calculate the number of points in a staircase sweep."""
        try:
            out = (abs((stop - start) // step) + 1)
        except ZeroDivisionError:
            out = 1
        return out

    def set_num_sweeps(self, sweeps: int) -> None:
        """Overridden in daughter classes in that allow multiple sweeps."""
        pass

    @abstractmethod
    def set_meas_rate(self, rate: int) -> None:
        """Set integration rate or equivalent for 6221/2182A to rate.

        For differential conductance and delta measurements, this is the
        integration rate of the 2182a.  For pulse delta measurements, this is
        the cycle interval (or period) of the measurement.  Refer to the
        manuals for more information.
        """
        pass

    def set_meas_delay(self, num: float) -> None:
        """Set the delay time between changing applied current and measurement.

        The delay time is a pause between when the 6221 applies a new current
        and when the 2182a measures a voltage, which gives the current time to
        settle.  The units of num vary between milliseconds and microseconds
        depending on the measurement type.
        """
        self.meas_delay = num

    def set_pulse_width(self, num: float) -> None:
        """Overridden in daughter classes that have pulse widths."""
        pass

    def set_low_meas(self, enable: bool) -> None:
        """Overridden in daughter classes that have a low measure option."""
        pass

    def set_filter_idx(self, idx: int) -> None:
        """Overridden in daughter classes that can specify the filter type."""
        pass

    def set_filter_on(self, enable: bool) -> None:
        """Enable or disable internal Keithley data filtering."""
        self.filter_on = enable

    def set_filter_window(self, wind: int) -> None:
        """Set the filter window to wind.

        Filter window is the percent deviation from the average that will not
        trigger starting a new filtering bin. Basically, the window tells the
        program what change in measurement it should consider a measurement of
        a different thing (e.g., applied current).
        """
        self.filter_window = wind

    def set_filter_count(self, count: int) -> None:
        """Set the number of measurements to average to count."""
        self.filter_count = count

    def get_total_points(self) -> None:
        """Overridden in daughter classes that have a number of sweeps."""
        return self.num_points

    def update_num_points(self) -> None:
        """Overridden in daughter classes for which this is important."""
        pass
