#!/usr/bin/env python2

import pygtk
pygtk.require('2.0')
import gtk
import os
from time import time
from math import floor
gtk.gdk.threads_init()
import gobject

YELLOW_AFTER = 60 * 24
GREEN_AFTER = 60 * 25
REYELLOW_AFTER = 60 * 49
OFF_AFTER = 60 * 50

class Pomodoro:
    def __init__(s):
        s.icon=gtk.status_icon_new_from_file(s.resource("phase-0.png"))
        s.icon.set_tooltip("Idle")
        s.state = "idle"
        s.tick_interval = 5 # number of seconds between each poll
        s.icon.connect('activate', s.icon_click)
        s.icon.set_visible(True)
        s.work_started = 0
        gobject.timeout_add(200, s.ding)
        s.update()

    def format_time(s, seconds):
        minutes = floor(seconds / 60)
        if minutes > 1:
            return "%d minutes" % minutes
        else:
            return "%d minute" % minutes

    def start_work(s):
        s.work_started = time()
        s.phase = 1
        s.state = "working"
        s.icon.set_from_file(s.resource("phase-1.png"))

    def start_idling(s):
        s.state = "idle"
        os.system('./set-skype-status online')
        s.icon.set_from_file(s.resource("phase-0.png"))
        s.icon.set_tooltip("Worked for %s." % s.format_time(time() - s.work_started))


    def resource(s, file_name):
        return os.path.dirname(os.path.realpath(__file__)) + os.path.sep + file_name

    def icon_click(s, _):
        delta = time() - s.work_started
        if s.state == "idle":
            os.system('./set-skype-status invisible')
            s.start_work()
        else:
            os.system('./set-skype-status online')
            s.start_idling()

    def triple_ding(s):
        s.ding()
        s.ding()
        s.ding()

    def ding(s, times = 1):
        os.system('aplay alarm.wav')

    def update(s):
        if s.state == "working":
            delta = time() - s.work_started
            s.icon.set_tooltip("Working for %s..." % s.format_time(delta))

            current_phase = 1
            if delta > YELLOW_AFTER:
                current_phase = 2
            if delta > GREEN_AFTER:
                current_phase = 3
            if delta > REYELLOW_AFTER:
                current_phase = 4
            if delta > OFF_AFTER:
                os.system('./set-skype-status online')
                s.icon.set_from_file( s.resource("phase-%d.png" % 0) )
                s.state = "idle"
                gobject.timeout_add(200, s.triple_ding)
            else:
                if s.phase != current_phase:
                    s.phase = current_phase
                    s.icon.set_from_file( s.resource("phase-%d.png" % current_phase) )
                    if current_phase == 3:
                        gobject.timeout_add(200, s.ding)

        gobject.timeout_add(s.tick_interval*1000, s.update)

    def main(s):
        gtk.main()

if __name__ == "__main__":
    Pomodoro().main()
