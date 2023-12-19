from .base_model import BaseModel
from typing import Optional, TYPE_CHECKING
from sqlmodel import Relationship


if TYPE_CHECKING:
    from .artist_album import ArtistAlbum


class Album(BaseModel, table=True):
    __tablename__ = 'albums'

    title: str
    artist_album: Optional['ArtistAlbum'] = Relationship(back_populates='album')
