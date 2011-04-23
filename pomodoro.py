#!/usr/bin/env python2
from __future__ import division

import pygtk
pygtk.require('2.0')
import gtk
from time import time
from math import floor
gtk.gdk.threads_init()
import gobject

#Parameters
MIN_WORK_TIME = 60 * 1 # min work time in seconds

class Pomodoro:
    def __init__(self):
        self.icon=gtk.status_icon_new_from_file("idle.svg")
        self.icon.set_tooltip("Idle")
        self.state = "idle"
        self.tick_interval=10 #number of seconds between each poll
        self.icon.connect('activate',self.icon_click)
        self.icon.set_visible(True)
        self.start_working_time = 0
    def format_time(self,seconds):
        minutes = floor(seconds / 60)
        if minutes > 1:
            return "%d minutes" % minutes
        else:
            return "%d minute" % minutes
    def set_state(self,state):
        old_state=self.state
        self.icon.set_from_file(state+".svg")
        if state == "idle":
            delta = time() - self.start_working_time
            if old_state == "ok":
                self.icon.set_tooltip("Good! worked for %s." % 
                        self.format_time(delta))
            elif old_state == "working":
                self.icon.set_tooltip("Not good: worked for only %s." % 
                        self.format_time(delta))
        else:
            self.start_working_time = time()
            delta = time() - self.start_working_time
            self.icon.set_tooltip("Working for %s..." % self.format_time(delta))
        self.state=state
    def icon_click(self,dummy):
        delta = time() - self.start_working_time
        if self.state == "idle":
            self.set_state("working")
        else:
            self.set_state("idle")
    def update(self):
        """This method is called everytime a tick interval occurs"""
        delta = time() - self.start_working_time
        if self.state == "idle":
            pass
        else:
            self.icon.set_tooltip("Working for %s..." % self.format_time(delta))
            if self.state == "working":
                if delta > MIN_WORK_TIME:
                    self.set_state("ok")
        source_id = gobject.timeout_add(self.tick_interval*1000, self.update)
    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        source_id = gobject.timeout_add(self.tick_interval, self.update)
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a Pomodoro instance and show it
if __name__ == "__main__":
    app = Pomodoro()
    app.main()
