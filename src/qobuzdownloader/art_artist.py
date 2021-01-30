# art_artist.py
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

from gi.repository import Gtk, Handy, Gdk, GdkPixbuf, Pango
from qobuzdownloader.help_task import TaskHelper

class ArtistBox(Gtk.FlowBoxChild):
    def __init__(self,artist):
        Gtk.FlowBoxChild.__init__(self)
        print(self.get_parent())
        self.artist = artist

        artist_name = Gtk.Label.new()
        artist_name.set_markup(f"<span font_weight='bold'>{artist.name}</span>")
        # artist_name.set_ellipsize(Pango.EllipsizeMode(3))
        artist_name.set_max_width_chars(10)
        artist_name.set_justify(Gtk.Justification.CENTER)
        artist_name.show()

        self.cover = Handy.Avatar.new(112,artist.name,True)
        self.cover.show()

        box = Gtk.Box.new(Gtk.Orientation(1),0)
        box.add(self.cover)
        box.add(artist_name)
        box.set_spacing(10)
        box.show()
        
        self.add(box)
        self.show()

    def display_cover(self,data,size=35):
        loader = GdkPixbuf.PixbufLoader.new()
        loader.write(data)
        loader.close()
        loader = loader.get_pixbuf()
        loader = loader.scale_simple(size,size,GdkPixbuf.InterpType.BILINEAR)
        self.cover.set_image_load_func(Handy.AvatarImageLoadFunc(size,loader))

class ArtistFlowBox(Gtk.FlowBox):
    def __init__(self,app):
        self.app = app
        Gtk.FlowBox.__init__(self)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.show()