from .base_sql_repository import BaseSqlRepository
from app.stores.sql_store import SqlStore
from app.models.song import Song


class SongsRepository(BaseSqlRepository):
    def __init__(self, store: SqlStore):
        super().__init__(store, Song)

    def get_many_with_join(self, secondary_model, key_name, *filters, page, per_page):
        target = getattr(self._model, key_name)
        return self._store.filter_with_join(self._model, secondary_model, target, *filters,
                                            page=page, per_page=per_page)
