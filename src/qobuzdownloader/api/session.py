# session.py
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

import time
import hashlib
import qobuzdownloader.api.spoofbuz as spoofbuz
from qobuzdownloader.api.request import Requests
from qobuzdownloader.api.models import Album, Artist, Track, Playlist

class Session():
    def __init__(self):
        self.id = 0
        self.base_url = "https://www.qobuz.com/api.json/0.2/"

    def login(self,email=None,pwd=None,token=None):
        spoofer = spoofbuz.Spoofer()
        self.id = spoofer.getAppId()
        self.request = Requests(self.id,"") #Key is set later
        params={
                "email": email,
                "password": pwd,
                "user_auth_token":token,
        }

        r = self.request.get(self.base_url+"user/login",'post',params=params)
        if r.status_code == 401:
            return False, True
        elif r.status_code == 400:
            return False, False
        result = r.json()
        self.uat = result["user_auth_token"]
        self.offer = result["user"]["subscription"]["offer"]
        if self.offer ==  "studio": # Set the maximum quality by default depending on the user's offer
            self.quality = 27
        else:
            self.quality = 6

        if result["user"]["firstname"] is None:
            self.username = result["user"]["display_name"]
        elif result["user"]["lastname"] is None:
            self.username = result["user"]["firstname"]
        else:
            self.username = result["user"]["firstname"] + " " + result["user"]["lastname"]

        self.user_id = result["user"]["id"]

        self.request.update_session("X-User-Auth-Token",self.uat)
        self.request.update_session("X-Store",result["user"]["store"])
        self.request.update_session("X-Zone",result["user"]["zone"])

        for secret in spoofer.getSecrets().values():
            if self.test_secret(secret):
                self.request.key = secret
                break
        return True

    def logoff(self):
        """ Log off:
            This overwrite the old request session by a new one """
        self.uat =  ""
        self.request = Requests(self.id,"")

    def test_secret(self,key):
        unix = time.time()
        r_sig = "userLibrarygetAlbumsList" + str(unix) + key
        r_sig_hashed = hashlib.md5(r_sig.encode('utf-8')).hexdigest()
        params={
            "app_id": self.id,
            "user_auth_token": self.uat,
            "request_ts": unix,
            "request_sig": r_sig_hashed}
        r = self.request.get(self.base_url+'userLibrary/getAlbumsList?',params=params)
        return r.ok

    def search(self,query,limit=100):
        params={
            "query": query,
            "limit": limit
        }
        r = self.request.get(self.base_url+"catalog/search",params=params)
        results = r.json()
        artists = list(map(lambda x: Artist(x),results["artists"]["items"]))
        tracks = list(map(lambda x: Track(x),results["tracks"]["items"]))
        albums = list(map(lambda x: Album(x),results["albums"]["items"]))
        # playlists = list(map(lambda x: Track(x),results["tracks"]["items"]))
        return albums, tracks, artists

    def get_album(self,id,limit=100,extra=None):
        params={
            "album_id": id,
            "limit": limit,
            "extra": extra
        }
        r = self.request.get(self.base_url+"album/get",params=params)
        return Album(r.json())

    def get_track(self,id,limit=100,extra=None):
        params={
            "track_id": id,
            "limit": limit,
            "extra": extra
        }
        r = self.request.get(self.base_url+"track/get",params=params)
        return Track(r.json())

    def get_artist(self,id,extra=None):
        params={
            "artist_id": id,
            "extra": extra
        }
        r = self.request.get(self.base_url+"artist/get",params=params)
        return Artist(r.json())
        
    def get_userfav_albums(self,limit=1000):
        params = {
            "limit" : limit,
            "type" : "albums",
            "user_id": self.user_id
        }
        r = self.request.get(self.base_url+"favorite/getUserFavorites",params=params)
        return list(map(lambda x: Album(x),r.json()["albums"]["items"]))

    def get_userfav_artists(self,limit=1000):
        params = {
            "limit" : limit,
            "type" : "artists",
            "user_id": self.user_id
        }
        r = self.request.get(self.base_url+"favorite/getUserFavorites",params=params)
        return list(map(lambda x: Artist(x),r.json()["artists"]["items"]))

    def get_userfav_tracks(self,limit=1000):
        params = {
            "limit" : limit,
            "type" : "tracks",
            "user_id": self.user_id
        }
        r = self.request.get(self.base_url+"favorite/getUserFavorites",params=params)
        return list(map(lambda x: Track(x),r.json()["tracks"]["items"]))

    def get_userfav_playlists(self,limit=1000):
        params = {
            "limit" : limit,
            "user_id": self.user_id
        }
        r = self.request.get(self.base_url+"playlist/getUserPlaylists",params=params)
        return list(map(lambda x: Playlist(x),r.json()["playlists"]["items"]))

    def get_streamable_url(self,track):
        """Quality:
            MP3: 5
            CD 16 bits/44.1kHz: 6
            HiRes 24 bits/96kHz: 7
            HiRes 24 bits/192kHz: 27
        """
        unix = time.time()
        r_sig = f"trackgetFileUrlformat_id{self.quality}intentstreamtrack_id{track.id}{unix}{self.request.key}"
        r_sig_hashed = hashlib.md5(r_sig.encode('utf-8')).hexdigest()
        params={
            "request_ts": unix,
            "request_sig": r_sig_hashed,
            "track_id": track.id,
            "format_id": self.quality,
            "intent": 'stream'}

        return self.request.get(self.base_url+"track/getFileUrl?",params=params).json()["url"]

    def get_cover_data(self,url):
        return self.request.get(url).content