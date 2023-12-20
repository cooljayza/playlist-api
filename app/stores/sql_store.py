from sqlmodel import create_engine, Session, select
from sqlalchemy import func
from sqlalchemy.orm.session import SessionTransaction


class SqlStore:
    def __init__(self, connection_string):
        self._connection_string = connection_string
        self.transaction: SessionTransaction = None
        self.session: Session = None

    def connect(self):
        self.session = Session(
            create_engine(self._connection_string, echo=True, connect_args={'check_same_thread': False}))

    def begin_transaction(self):
        self.transaction = self.session.begin()

    def commit_transaction(self):
        if self.transaction:
            self.transaction.commit()
            self.transaction = None

    def rollback_transaction(self):
        if self.transaction:
            self.transaction.rollback()
            self.transaction = None

    def insert(self, entity):
        self.session.add(entity)
        self._save()
        self.session.refresh(entity)
        return entity

    def insert_many(self, entities):
        self.session.add_all(entities)
        self._save()

        return entities

    def find(self, model, identifier):
        statement = select(model).where(model.id == identifier)
        result = self.session.exec(statement)
        return result

    def update(self, entity):
        self.session.add(entity)
        self._save()
        self.session.refresh(entity)
        return entity

    def update_many(self, entities):
        self.session.add_all(entities)
        self._save()
        return entities

    def remove(self, entity):
        self.session.delete(entity)
        self._save()
        return entity

    def filter(self, model, *where_statements, joins=None, page, per_page):
        limit = per_page * page
        offset = (page - 1) * per_page
        query = select(model).limit(limit).offset(offset).where(*where_statements)
        if joins:
            for join in joins:
                query = query.join(*join)
        results = self.session.exec(query)
        count = self.session.scalar(select(func.count(model.id)).select_from(query.alias()))

        return {'items': results, 'count': count}

    def _save(self):
        self.session.commit()
