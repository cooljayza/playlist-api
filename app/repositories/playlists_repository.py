from app.models.playlist import Playlist
from app.stores.sql_store import SqlStore
from .base_sql_repository import BaseSqlRepository


class PlaylistsRepository(BaseSqlRepository):
    def __init__(self, store: SqlStore):
        super().__init__(store, Playlist)

    def get_many_with_two_joins(self, secondary_model, tertiary_model, primary_key, secondary_key, *filters, page,
                                per_page):
        primary_target = getattr(self._model, primary_key)
        secondary_target = getattr(secondary_model, secondary_key)

        return self._store.filter_with_two_joins(self._model, secondary_model, tertiary_model, primary_target,
                                                 secondary_target, *filters, page=page, per_page=per_page)
