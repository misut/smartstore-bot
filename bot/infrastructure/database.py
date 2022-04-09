import sqlalchemy
from sqlalchemy import orm

from bot.infrastructure.orm import OrmBase

_DATABASE_URL = "sqlite:///.smartstore_bot.db?check_same_thread=False"


class SqlAlchemyDatabase:
    engine: sqlalchemy.engine
    session_factory: orm.sessionmaker

    def __init__(self, url: str = _DATABASE_URL) -> None:
        self.engine = sqlalchemy.create_engine(url=url)
        self.session_factory = orm.sessionmaker(bind=self.engine)

    def session(self) -> orm.Session:
        return self.session_factory()

    def create_all(self) -> None:
        OrmBase.metadata.create_all(self.engine)

    def drop_all(self) -> None:
        OrmBase.metadata.drop_all(self.engine)
