# window.py
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

from gi.repository import Gtk, Handy, Gdk

from qobuzdownloader.api.session import Session
from qobuzdownloader.help_task import TaskHelper
from qobuzdownloader.art_track import TrackListBox, TrackRow
from qobuzdownloader.art_artist import ArtistFlowBox, ArtistBox
from qobuzdownloader.help_artwork import get_cover_from_album


@Gtk.Template(resource_path='/com/github/Aurnytoraink/QobuzDownloader/ui/window.ui')
class QobuzdownloaderWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'QobuzdownloaderWindow'

    main_stack = Gtk.Template.Child()

    #Login page
    log_user = Gtk.Template.Child()
    log_pwd = Gtk.Template.Child()
    destination_select = Gtk.Template.Child()
    log_btn = Gtk.Template.Child()
    log_error_reveal = Gtk.Template.Child()
    log_error_label = Gtk.Template.Child()
    log_stack = Gtk.Template.Child()
    forget_pwd_btn = Gtk.Template.Child()

    #Search page
    search_entry = Gtk.Template.Child()
    app_stack = Gtk.Template.Child()
    track_viewport = Gtk.Template.Child()
    artist_viewport = Gtk.Template.Child()
    album_viewport = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_btn.connect("clicked",self.login_username)
        self.log_user.connect("changed",self.update_login_page)
        self.log_pwd.connect("changed",self.update_login_page)
        self.forget_pwd_btn.connect("clicked",self.forget_pwd)
        self.search_entry.connect("search-changed",self.get_search)

        #Init session
        self.session = Session()

        self.track_listbox = TrackListBox(self)
        self.track_viewport.add(self.track_listbox)

        self.artist_flowbox = ArtistFlowBox(self)
        self.artist_viewport.add(self.artist_flowbox)



### Login
    def login_username(self,*_):
        self.log_error_reveal.set_reveal_child(False)
        self.log_user.set_sensitive(False)
        self.log_pwd.set_sensitive(False)
        self.log_btn.set_sensitive(False)
        self.destination_select.set_sensitive(False)
        self.log_stack.set_visible_child_name("try")
        TaskHelper().run(self.session.login,self.log_user.get_text(), self.log_pwd.get_text(),callback=(self.on_login,))

    def on_login(self,state):
        def on_login_sucess():
            self.main_stack.set_visible_child_name("app_page")
            self.log_user.set_text("") # Remove content in case
            self.log_pwd.set_text("")

        def on_login_unsucess(error,show):
            self.log_error_label.set_text(error)
            self.log_error_reveal.set_reveal_child(True)

        # Reset interface
        self.log_user.set_sensitive(True)
        self.log_pwd.set_sensitive(True)
        self.log_btn.set_sensitive(True)
        self.destination_select.set_sensitive(True)
        self.log_stack.set_visible_child_name("label")

        if type(state) == bool:
            on_login_sucess()
        else:
            if state[1]:
                on_login_unsucess("Wrong email/password",True)
            else:
                on_login_unsucess("A internal error occured",False)

    def forget_pwd(self,*_):
        Gtk.show_uri_on_window(self,"https://www.qobuz.com/reset-password",Gdk.CURRENT_TIME)

    def update_login_page(self,*_):
        self.log_error_reveal.set_reveal_child(False)
        if self.log_user.get_text() == "" or self.log_pwd.get_text() == "":
            self.log_btn.set_sensitive(False)
        else:
            self.log_btn.set_sensitive(True)


### Interface

    def get_search(self,search):
        query = search.get_text()
        if query != "":
            self.app_stack.set_visible_child_name("wait")
            self.clear_all()
            TaskHelper().run(self.session.search,query,callback=(self.display_search,))
        else:
            self.app_stack.set_visible_child_name("home")

    def display_search(self,results):
        self.app_stack.set_visible_child_name("app")
        for track in results[1]:
            row = TrackRow(track)
            self.track_listbox.add(row)
            TaskHelper().run(get_cover_from_album,row.track,self.session,callback=(row.display_cover,))
        for track in results[2]:
            box = ArtistBox(track)
            self.artist_flowbox.add(box)

    def clear_all(self,*args):
        for child in self.track_listbox.get_children(): child.destroy()
        for child in self.artist_flowbox.get_children(): child.destroy()