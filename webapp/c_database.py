
from pathlib import Path
import c_config as wacfg

from flask import Flask  # noqa
from flask_sqlalchemy import SQLAlchemy

database: SQLAlchemy


class CDatabase:
    """Класс для работы с БД."""

    def __init__(self, papplication: Flask):
        self.engine = None
        self.session = None
        global database
        database = SQLAlchemy(papplication)
        self.connect()
        if not self.exists():

            self.create()

    def connect(self):
        """Устанавливает соединение с БД."""
        self.engine = database.create_engine(wacfg.Config.SQLALCHEMY_DATABASE_URI,
                                                  echo=wacfg.Config.ALCHEMY_ECHO,
                                                  connect_args={'check_same_thread': False})
        session = database.sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()
        database.Base.metadata.bind = self.engine

    def create(self):
        """Создаёт базу данных."""
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        database.Base.metadata.create_all()

    def exists(self):  # noqa
        """Проверяет наличие базы данных по пути в конфигурации."""
        return Path(wacfg.Config.DB_PATH + wacfg.Config.DB_NAME).exists()
