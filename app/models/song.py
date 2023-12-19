from .base_model import BaseModel
from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING, List


if TYPE_CHECKING:
    from .artist_album import ArtistAlbum


class Song(BaseModel, table=True):
    __tablename__ = 'songs'

    title: str
    rank: int = Field(unique=True)
    artist_album_id: Optional[int] = Field(default=None, foreign_key='artist_albums.id')
    artist_album: Optional['ArtistAlbum'] = Relationship(back_populates='songs')

