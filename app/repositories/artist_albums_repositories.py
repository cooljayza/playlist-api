from .base_sql_repository import BaseSqlRepository
from app.models.artist_album import ArtistAlbum
from app.stores.sql_store import SqlStore


class ArtistAlbumsRepositories(BaseSqlRepository):
    def __init__(self, store: SqlStore):
        super().__init__(store, ArtistAlbum)
