from __future__ import annotations

from datetime import datetime
from loguru import logger

import sqlalchemy
from sqlalchemy import orm

from bot.domain import Account, AccountRepository
from bot.infrastructure.database import SqlAlchemyDatabase
from bot.infrastructure.orm import OrmBase


class AccountOrm(OrmBase):
    __tablename__ = "accounts"

    id = sqlalchemy.Column(sqlalchemy.String(128), primary_key=True)
    password = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now, nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now, nullable=False)

    @classmethod
    def from_entity(cls, entity: Account) -> AccountOrm:
        return cls(
            id=entity.id,
            password=entity.password,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class SqlAccountRepository(AccountRepository):
    database: SqlAlchemyDatabase
    session: orm.Session = None

    class Config:
        arbitrary_types_allowed = True

    def __enter__(self) -> AccountRepository:
        self.session = self.database.session()
        return super().__enter__()

    def __exit__(self, *args) -> None:
        super().__exit__(*args)
        self.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()
    
    def rollback(self) -> None:
        self.session.rollback()

    def select(self) -> list[Account]:
        fetched = self.session.query(AccountOrm).all()
        return [Account.from_orm(obj) for obj in fetched]

    def get(self, entity_id: str) -> Account | None:
        fetched = self.session.query(AccountOrm).filter_by(id=entity_id).one_or_none()
        if not fetched:
            return None
        return Account.from_orm(fetched)

    def insert(self, entity: Account) -> None:
        obj = AccountOrm.from_entity(entity)
        self.session.add(obj)
        self.session.flush()

    def update(self, entity: Account) -> None:
        fetched = self.session.query(AccountOrm).filter_by(id=entity.id).one_or_none()
        if not fetched:
            return None
        
        fetched.password = entity.password
        fetched.updated_at = entity.updated_at
        self.session.flush()

    def delete(self, entity_id: str) -> None:
        self.session.query(AccountOrm).filter_by(id=entity_id).delete()
        self.session.flush()
