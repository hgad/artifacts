#!/usr/bin/env python

"""
Author: Haitham Gad
Date: JUN 7, 2014
Description: Sleep calculator.
"""

import sys
import getopt
import datetime

class Usage(Exception):
  def __init__(self, prog, msg):
    self.msg = msg
    self.prog = prog

  def usage(self):
    print >>sys.stderr, "Usage:\n"
    print >>sys.stderr, ("  " + self.prog +
        "        - Prints the times you should wake up at if you go to sleep now.")
    print >>sys.stderr, ("  " + self.prog +
        " [time] - Prints the times you should go to sleep if you wish to wake up at 'time'.")
    print >>sys.stderr, "\nExamples of [time]: 4:50am, 6:30pm."

class SleepCalc(object):
  def __init__(self, prog, wake_up_time = ""):
    self.prog = prog
    self.fall_asleep = datetime.timedelta(minutes = 14)
    self.cycle = datetime.timedelta(minutes = 90)

    if wake_up_time:
      try:
        self.wake_up_time = datetime.datetime.strptime(wake_up_time, "%I:%M%p")
      except ValueError:
        raise Usage(self.prog, "Invalid time format")

  def time_to_string(self, time):
    return time.strftime("%I:%M %p")

  def when_to_wake_up(self, sleep_time):
    return map((lambda n: sleep_time + self.fall_asleep + n * self.cycle),
               range(3, 7))

  def when_to_sleep(self, wake_time):
    return map((lambda n: wake_time - n * self.cycle - self.fall_asleep),
               range(3, 7))

  def wake_up(self):
    print "If you go to sleep now, you should wake up at one of the following times:\n"
    for t in (dt.time() for dt in self.when_to_wake_up(datetime.datetime.now())):
      print self.time_to_string(t)
    print

  def sleep(self):
    print ("If you wish to wake up at " + self.time_to_string(self.wake_up_time) +
           ", you should sleep at one of the following times:\n")
    for t in (dt.time() for dt in self.when_to_sleep(self.wake_up_time)):
      print self.time_to_string(t)
    print

def main(argv=None):
  if argv is None:
    argv = sys.argv

  try:
    try:
      opts, args = getopt.getopt(argv[1:], "h", ["help"])

    except getopt.error, msg:
      raise Usage(argv[0], msg)

    for o, a in opts:
      if o in ("-h", "--help"):
        Usage(argv[0], "").usage()
        return 0

    if not args:
      SleepCalc(argv[0]).wake_up()
    else:
      SleepCalc(argv[0], args[0]).sleep()

  except Usage, err:
    print >>sys.stderr, "Error: " + err.msg
    err.usage()
    return 2

if __name__ == "__main__":
  sys.exit(main())

