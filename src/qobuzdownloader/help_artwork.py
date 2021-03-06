# help_artwork.py
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

import os

from qobuzdownloader.api.models import Track

def get_cover_from_album(item,session):
    if type(item) == Track:
        id = item.album.id
    else:
        id = item.id
    try:
        if os.path.isfile(f'/var/cache/files/covers/album_{id}.jpg') is False:
            data = session.get_cover_data(item.cover)
            open(f'/var/cache/files/covers/album_{id}.jpg','xb').write(data)
        else:
            data = open(f'/var/cache/files/covers/album_{id}.jpg','rb').read()
    except:
        data = open(f'/var/cache/files/covers/album_{id}.jpg','rb').read()
    return data

def get_cover_from_artist(item,session):
    if os.path.isfile(f'/var/cache/files/covers/artist_{item.id}.jpg') is False:
        data = session.get_cover_data(item.cover)
        open(f'/var/cache/files/covers/artist_{item.id}.jpg','xb').write(data)
    else:
        data = open(f'/var/cache/files/covers/artist_{item.id}.jpg','rb').read()
    return data