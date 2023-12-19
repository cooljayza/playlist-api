from app.models.artist import Artist
from app.stores.sql_store import SqlStore
from .base_sql_repository import BaseSqlRepository


class ArtistsRepository(BaseSqlRepository):
    def __init__(self, store: SqlStore):
        super().__init__(store, Artist)
