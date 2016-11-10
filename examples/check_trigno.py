"""
Tests communication with and data acquisition from a Delsys Trigno wireless
EMG system. Delsys Trigno Control Utility needs to be installed and running,
and the device needs to be plugged in. Tests can be run with a device connected
to a remote machine if needed.

The tests run by this script are very simple and are by no means exhaustive. It
just sets different numbers of channels and ensures the data received is the
correct shape.

Use `-h` or `--help` for options.
"""

import argparse
from axopy import daq


def check_emg(host):
    dev = daq.TrignoEMG(channel_range=(0, 0), samples_per_read=270,
                        host=host)

    # test single-channel
    dev.start()
    for i in range(4):
        data = dev.read()
        assert data.shape == (1, 270)
    dev.stop()

    # test multi-channel
    dev.set_channel_range((0, 4))
    dev.start()
    for i in range(4):
        data = dev.read()
        assert data.shape == (5, 270)
    dev.stop()


def check_accel(host):
    dev = daq.TrignoAccel(channel_range=(0, 2), samples_per_read=10,
                          host=host)

    dev.start()
    for i in range(4):
        data = dev.read()
        assert data.shape == (3, 10)
    dev.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-a', '--addr',
        dest='host',
        default='localhost',
        help="IP address of the machine running TCU. Default is localhost.")
    args = parser.parse_args()

    check_emg(args.host)
    check_accel(args.host)
