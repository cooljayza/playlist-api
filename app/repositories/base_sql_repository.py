from app.stores.sql_store import SqlStore


class BaseSqlRepository:
    def __init__(self, store: SqlStore, model):
        self._model = model
        self._store = store

    def add(self, entity):
        return self._store.insert(entity)

    def add_many(self, entities):
        return self._store.insert_many(entities)

    def update(self, entity):
        return self._store.update(entity)

    def update_many(self, entities):
        return self._store.update_many(entities)

    def delete(self, entity):
        return self._store.remove(entity)

    def get_by_id(self, identifier):
        return self._store.find(self._model, identifier)

    def get_many(self, *where_clause, page=1, per_page=100, joins=None):
        return self._store.filter(self._model, *where_clause, page=page, per_page=per_page, joins=joins)

    def begin_transaction(self):
        self._store.begin_transaction()

    def commit_transaction(self):
        self._store.commit_transaction()

    def rollback_transaction(self):
        self._store.rollback_transaction()
