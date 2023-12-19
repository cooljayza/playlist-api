from app.models.playlist import Playlist
from app.stores.sql_store import SqlStore
from .base_sql_repository import BaseSqlRepository


class PlaylistsRepository(BaseSqlRepository):
    def __init__(self, store: SqlStore):
        super().__init__(store, Playlist)
