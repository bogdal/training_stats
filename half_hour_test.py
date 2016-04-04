#!/usr/bin/env python3

import sys
from xml.dom.minidom import parse
from operator import itemgetter
from datetime import datetime

import matplotlib.pyplot as pyplot
import numpy as np

def get_time(trkpt):
    time_children = trkpt.getElementsByTagName("time")
    if time_children:
        return time_children[0].childNodes[0].toxml()


def get_hr(trkpt):
    hr_children = trkpt.getElementsByTagName('gpxtpx:hr')
    if hr_children:
        return int(hr_children[0].childNodes[0].wholeText)


def decode_iso_time(timestr):
    return datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%SZ')


def convert_time(time, start):
    """ Calculates elapsed timed from start in second """
    dt = decode_iso_time(time) - start
    return int(dt.total_seconds())


def get_trkpts(gpx_file):
    """ Retrieves all trkpt from gpx_file. Returns list of DOM elements."""
    gpx = parse(gpx_file)
    return gpx.childNodes[0].getElementsByTagName("trkpt")


def get_hr_measurements(gpx_file):
    """ Generates list of (t, hr) from gpx. Skips missing measuruments. """
    data = [(get_time(p), get_hr(p)) for p in get_trkpts(gpx_file)]
    start_time = decode_iso_time(data[0][0])
    return [(convert_time(t, start_time), hr) for (t, hr) in data if hr]


def interpolate(points):
    time, hr = zip(*points)
    end_time = time[-1]
    new_time = np.arange(int(time[-1]))
    return list(zip(new_time, np.interp(new_time, time, hr)))


def calculate_moving_sums(points, window):
    """ Calculates hr moving sums of the window len """
    time, hrs = zip(*points)
    moving_sum = sum(hrs[0:window])
    sums = [(time[0], moving_sum)]
    for i, t in enumerate(time[1:-1*window]):
        moving_sum += hrs[i+window]-hrs[i]
        sums.append((t, moving_sum))
    return sums


def main():
    test_period = 60 * 30      # test time
    measured_period = 60 * 20  # measured period in seconds
    plot_hr = True             # turn off to disable data plotting

    gpx_file = sys.argv[1]
    print("Loading gpx: {}".format(gpx_file))

    hrs = interpolate(get_hr_measurements(gpx_file))
    time_stamp, max_sum = max(calculate_moving_sums(hrs, test_period),
                              key=itemgetter(1))

    # your lactate threshold is average of last 20 in 30 minutes of tempo run
    start_measure = time_stamp + (test_period - measured_period)
    stop_measure = start_measure + measured_period
    measured_time, measured_hrs = zip(*hrs[start_measure:stop_measure])
    lactate_thr = round(sum(measured_hrs) / measured_period)

    print("Your lactate threshold is {} bpm.".format(lactate_thr))

    if(plot_hr):
        pyplot.plot(*zip(*hrs), 'b')
        pyplot.plot(measured_time, measured_hrs, 'r')
        pyplot.show()


if __name__ == "__main__":
    main()