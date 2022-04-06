from __future__ import annotations

from datetime import datetime

import sqlalchemy
from sqlalchemy import orm

from bot.domain import Account, AccountRepository
from bot.infrastructure.orm import OrmBase


class AccountOrm(OrmBase):
    __tablename__ = "accounts"

    id = sqlalchemy.Column(sqlalchemy.String(128), primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)

    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now, nullable=False)

    @classmethod
    def from_entity(cls, entity: Account) -> AccountOrm:
        return cls(
            id=entity.id,
            username=entity.username,
            password=entity.password,
            updated_at=entity.updated_at,
        )


class SqlAccountRepository(AccountRepository):
    session: orm.Session

    def __enter__(self) -> AccountRepository:
        return super().__enter__()

    def __exit__(self, *args) -> None:
        self.session.rollback()
        super().__exit__(*args)

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
        fetched = self.get(entity.id)
        if not fetched:
            return None
        
        fetched.password = entity.password
        fetched.updated_at = entity.updated_at
        self.session.flush()

    def delete(self, entity_id: str) -> None:
        self.session.query(AccountOrm).filter_by(id=entity_id).delete()
        self.session.flush()
