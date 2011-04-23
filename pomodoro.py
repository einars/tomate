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

    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def hello(self, widget, data=None):
        print "Hello World"

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    # Another callback
    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        self.window.connect("delete_event", self.delete_event)

        # Here we connect the "destroy" event to a signal handler.
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        self.window.connect("destroy", self.destroy)

        # Sets the border width of the window.
        self.window.set_border_width(10)

        # Creates a new button with the label "Hello World".
        self.button = gtk.Button("Hello World")

        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        self.button.connect("clicked", self.hello, None)

        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)

        # This packs the button into the window (a GTK container).
        self.window.add(self.button)

        # The final step is to display this newly created widget.
        self.button.show()

        # and the window
        # self.window.show()
        self.icon=gtk.status_icon_new_from_file("acorn.svg")
        self.icon.set_tooltip("Idle")
        self.state = "IDLE"
        self.tick_interval=10 #number of seconds between each poll
        self.icon.connect('activate',self.icon_click)
        self.icon.set_blinking(False)
        self.icon.set_visible(True)
        self.start_working_time = 0
    def format_time(self,seconds):
        minutes = floor(seconds / 60)
        if minutes > 1:
            return "%d minutes" % minutes
        else:
            return "%d minute" % minutes
    def icon_click(self,dummy):
        delta = time() - self.start_working_time
        if self.state == "IDLE":
            self.state = "WORKING"
            self.start_working_time = time()
            self.icon.set_blinking(True)
            self.icon.set_tooltip("Working...")
        else:
            if self.state == "WORKING":
                self.icon.set_blinking(False)
                self.icon.set_tooltip("Not good: worked only %s." % 
                        self.format_time(delta))
            elif self.state == "OK":
                self.icon.set_tooltip("Good! worked %s." % 
                        self.format_time(delta))
            self.state="IDLE"
    def update(self):
        """This method is called everytime a tick interval occurs"""
        delta = time() - self.start_working_time
        if self.state == "IDLE":
            pass
        else:
            self.icon.set_tooltip("Working since %s..." % self.format_time(delta))
            if self.state == "WORKING":
                if delta > MIN_WORK_TIME:
                    self.state = "OK"
                    self.icon.set_blinking(False)
            elif self.state == "OK":
                pass
        #print "working..."
        #if not self.icon.get_visible(): #apres 5 minutes consecutives de glande, on montre l'icone
        #    self.icon.set_visible(True)
        #elif self.icon.get_visible():
        #    self.icon.set_visible(False)

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
