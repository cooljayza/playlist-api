from pydantic import BaseModel
from .song_schema import SongResponse
from typing import Optional


class PlaylistSongResponse(BaseModel):
    rank: int
    song: Optional[SongResponse]
