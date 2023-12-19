from pydantic import BaseModel
from .song_schema import SongResponse
from .create_playlist import CreatePlaylistResponse
from typing import Optional


class CreatePlaylistSongRequest(BaseModel):
    song_id: int


class CreatePlaylistSongResponse(BaseModel):
    playlist: Optional[CreatePlaylistResponse]
    song: Optional[SongResponse]
    rank: int
