#!/usr/bin/env python

from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
from gi.repository import AppIndicator3 as appindicator

import subprocess, re
import signal


APPINDICATOR_ID = "indicator-microphone"

MUTED_IMG = "/opt/indicator-microphone/img/muted.svg"
UNMUTED_IMG = "/opt/indicator-microphone/img/unmuted.svg"


class PeriodicTimer(object):
    _indicator = None

    def __init__(self, indicator, timeout=1):
        self._indicator = indicator
        self.callback()
        gobject.timeout_add_seconds(timeout, self.callback)

    def callback(self):
        try:
            re.split(" |:|\n", subprocess.check_output("pacmd list-sources | grep muted", shell=True)).index("yes")
            self._indicator.set_icon(MUTED_IMG)
        except:
            self._indicator.set_icon(UNMUTED_IMG)
        finally:
            return True


def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem("Quit")
    item_quit.connect("activate", quit)
    menu.append(item_quit)
    menu.show_all()
    return menu
 
def quit(source):
    gtk.main_quit()

def main():
    # Create indicator.
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, "/usr/share/icons/ubuntu-mono-dark/status/24/audio-input-microphone-high-panel.svg", appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())


    # Priodic timer to fetch state.
    timer = PeriodicTimer(indicator, 1)


    # Gtk main loop.
    gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
