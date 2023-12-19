from .base_model import BaseModel
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship


if TYPE_CHECKING:
    from .playlist_song import PlaylistSong


class Playlist(BaseModel, table=True):
    __tablename__ = 'playlists'

    name: str = Field(unique=True)
    playlist_songs: List['PlaylistSong'] = Relationship(back_populates='playlist')
