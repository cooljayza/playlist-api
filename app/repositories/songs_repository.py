from .base_sql_repository import BaseSqlRepository
from app.stores.sql_store import SqlStore
from app.models.song import Song


class SongsRepository(BaseSqlRepository):
    def __init__(self, store: SqlStore):
        super().__init__(store, Song)
