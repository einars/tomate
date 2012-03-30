#!/usr/bin/env python2

import pygtk
pygtk.require('2.0')
import gtk
import os
from time import time
from math import floor
gtk.gdk.threads_init()
import gobject

YELLOW_AFTER = 60 * 9
GREEN_AFTER = 60 * 44
#YELLOW_AFTER = 4
#GREEN_AFTER = 9

class Pomodoro:
    def __init__(s):
        s.icon=gtk.status_icon_new_from_file(s.resource("idle.png"))
        s.icon.set_tooltip("Idle")
        s.state = "idle"
        s.tick_interval = 5 # number of seconds between each poll
        s.icon.connect('activate', s.icon_click)
        s.icon.set_visible(True)
        s.work_started = 0
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
        s.icon.set_from_file(s.resource("idle.png"))
        s.icon.set_tooltip("Worked for %s." % s.format_time(time() - s.work_started))


    def resource(s, file_name):
        return os.path.dirname(os.path.realpath(__file__)) + os.path.sep + file_name

    def icon_click(s, _):
        delta = time() - s.work_started
        if s.state == "idle":
            s.start_work()
        else:
            s.start_idling()

    def ding(s):
        os.system('aplay %s' % s.resource('ding.wav'))

    def update(s):
        if s.state == "working":
            delta = time() - s.work_started
            s.icon.set_tooltip("Working for %s..." % s.format_time(delta))

            current_phase = 1
            if delta > YELLOW_AFTER:
                current_phase = 2
            if delta > GREEN_AFTER:
                current_phase = 3


            if s.phase != current_phase:
                s.phase = current_phase
                s.icon.set_from_file( s.resource("phase-%d.png" % current_phase) )
                if current_phase == 3:
                    gobject.timeout_add(300, s.ding)

        gobject.timeout_add(s.tick_interval*1000, s.update)

    def main(s):
        gtk.main()

if __name__ == "__main__":
    Pomodoro().main()
