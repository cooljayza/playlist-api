from pydantic import BaseModel


class PlaylistSongSwap(BaseModel):
    song1_id: int
    song2_id: int
