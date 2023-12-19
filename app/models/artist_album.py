from .base_model import BaseModel
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import Field, Relationship


if TYPE_CHECKING:
    from app.models.artist import Artist
    from app.models.album import Album
    from app.models.song import Song


class ArtistAlbum(BaseModel, table=True):
    __tablename__ = 'artist_albums'

    artist_id: Optional[int] = Field(default=None, foreign_key='artists.id')
    album_id: Optional[int] = Field(default=None, foreign_key='albums.id')
    year: int
    artist: Optional['Artist'] = Relationship(back_populates='artist_albums')
    album: Optional['Album'] = Relationship(back_populates='artist_album')
    songs: List['Song'] = Relationship(back_populates='artist_album')
