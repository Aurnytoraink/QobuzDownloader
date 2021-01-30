# main.py
#
# Copyright 2020 Aurnytoraink
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')

from gi.repository import Gtk, Handy, Gio

from .window import QobuzdownloaderWindow


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.github.Aurnytoraink.QobuzDownloader',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        Handy.init()

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.do_quit)
        self.add_action(action)

        self.set_accels_for_action("app.quit", ["<Ctl>q"])

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = QobuzdownloaderWindow(application=self)
        win.present()

        #Setup CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/com/github/Aurnytoraink/QobuzDownloader/css/style.css')
        Gtk.StyleContext.add_provider_for_screen(
            win.get_screen(), css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def do_quit(self,*_):
        self.quit()

def main(version):
    app = Application()
    return app.run(sys.argv)
