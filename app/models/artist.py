from .base_model import BaseModel
from typing import List, TYPE_CHECKING
from sqlmodel import Relationship


if TYPE_CHECKING:
    from .artist_album import ArtistAlbum


class Artist(BaseModel, table=True):
    __tablename__ = 'artists'

    name: str
    artist_albums: List['ArtistAlbum'] = Relationship(back_populates='artist')
