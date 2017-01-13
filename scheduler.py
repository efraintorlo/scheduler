# -*- coding: utf-8 -*-
# ---------------------------------------------------------
#     File:        scheduler.py
#     Author:      elchinot7
#     Email:       efraazu@gmail.com
#     Github:      https://github.com/elchinot7/scheduler
# ---------------------------------------------------------
"""
scheduler.py - Run an executable code without interfer with other Users
               The executable is active during the Night, Day or All day.

Author: Efrain Torres

Example: python scheduler.py -e executable
"""
from __future__ import print_function
import psutil
import datetime
import time
import sys
import optparse


_run_at = "night"

_morning = datetime.time(hour=6, minute=0)
_night = datetime.time(hour=21, minute=0)
_mid_night = datetime.time(hour=0, minute=0)


__version__ = "0.1"

_DEBUG = True


def am_I_alone():
    """Check that nobody is logged in this machine. """
    users = []
    for user in psutil.users():
        if user.name not in users:
            users.append(user.name)
    return len(users) == 1


def is_night():
    now = datetime.datetime.now()
    return now.time() < _morning


def is_day():
    now = datetime.datetime.now()
    return now.time() > _morning


def is_time_to_run(window):
    if window == 'night':
        return is_night()
    if window == 'day':
        return is_day()
    if window == '24':
        return True
    return False


def pid_exists(pid):
    # print(psutil.pid_exists(pid))
    return psutil.pid_exists(pid)


def get_pid(program):
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name() == program:
            print("\nPID: {}\n".format(pid))
            return pid
    return None


def get_status(pid):
    p = psutil.Process(pid)
    # print(p.status())
    return p.status()


def resurrect(pid):
    p = psutil.Process(pid)
    p.resume()
    print("Process: {} RESTARTED at {}".format(pid, datetime.datetime.now()))


def keep_quiet(pid):
    p = psutil.Process(pid)
    p.suspend()
    print("Process: {} PAUSED at {}".format(pid, datetime.datetime.now()))


def killall(pid):
    p = psutil.Process(pid)
    # p.terminate()
    # p.wait()
    p.kill()
    print("Process: {} KILLED at {}".format(pid, datetime.datetime.now()))


def schedule(program="spotify", run_at=_run_at, chances=10):
    fails = 0
    pid = get_pid(program)
    while True:
        if pid_exists(pid):
            if is_time_to_run(run_at) and am_I_alone():
                status = get_status(pid)
                if status is "stopped":
                    resurrect(pid)
                print("Hey mate, {} is running at nigth and you are alone, sorry!".format(program.upper()))
                # keep_quiet(pid)
                # killall(pid)
                fails = 0
            else:
                keep_quiet(pid)
        else:
            fails += 1
            time.sleep(2)
            if _DEBUG:
                print('FAILS: {}'.format(fails))
            if fails >= chances:
                sys.exit("\n{} is not running.\n".format(program))
        time.sleep(2)


def main(argv=None):
    if not argv:
        argv = sys.argv

    usage = "\n\t%prog -e executable -t night\n" + __doc__

    parser = optparse.OptionParser(usage=usage, version=__version__)

    parser.add_option("-e", "--executable", action="store", dest="executable",
                      type="string", metavar="STRING",
                      help="Executable program to follow.")

    parser.add_option("-t", "--time", action="store", dest="run_at",
                      default="night", type="string", metavar="STRING",
                      help="Keep active period, valid: day, night, 24")

    (options, args) = parser.parse_args(args=argv[1:])

    if not options.executable:
        parser.error("Executable not given.")

    print("\nThe program: {} will try to run at: {}.".format(options.executable,
                                                             options.run_at))

    schedule(options.executable, run_at=options.run_at)


if __name__ == "__main__":

    main()
