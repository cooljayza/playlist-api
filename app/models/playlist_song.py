from .base_model import BaseModel
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, UniqueConstraint


if TYPE_CHECKING:
    from .playlist import Playlist
    from .song import Song


class PlaylistSong(BaseModel, table=True):
    __tablename__ = 'playlist_songs'

    playlist_id: Optional[int] = Field(default=None, foreign_key='playlists.id')
    play_count: int = Field(default=0)
    isActive: bool = Field(default=True)
    rank: int
    song_id: Optional[int] = Field(default=None, foreign_key='songs.id')
    playlist: Optional['Playlist'] = Relationship(back_populates='playlist_songs')


