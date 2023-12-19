from pydantic import BaseModel
from app.models.song import Song
from typing import Optional


class ArtistResponse(BaseModel):
    name: str
    id: int


class AlbumResponse(BaseModel):
    title: str
    id: int


class SongResponse(BaseModel):
    title: Optional[str]
    id: Optional[int]
    artist: Optional[ArtistResponse]
    album: Optional[AlbumResponse]
    year: Optional[int]

    def from_model(self, model: Song):
        self.title = model.title
        self.id = model.id
        self.album = AlbumResponse(id=model.artist_album.album_id, title=model.artist_album.album.title)
        self.artist = ArtistResponse(id=model.artist_album.artist_id, name=model.artist_album.artist.name)
        self.year = model.artist_album.year

        return self
