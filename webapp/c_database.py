
from pathlib import Path
from webapp import c_config as wacfg

from flask import Flask  # noqa
from flask_sqlalchemy import SQLAlchemy


class CDatabaseManager:
    """Класс для работы с БД."""

    def __init__(self, pdatabase: SQLAlchemy):
        self.database: SQLAlchemy = pdatabase
        self.engine = None
        self.session = None
        self.connect()
        if not self.exists():

            self.create()

    def connect(self):
        """Устанавливает соединение с БД."""
        self.engine = self.database.create_engine(wacfg.Config.SQLALCHEMY_DATABASE_URI,
                                                  echo=wacfg.Config.ALCHEMY_ECHO,
                                                  connect_args={'check_same_thread': False})
        session = self.database.sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()
        self.database.Base.metadata.bind = self.engine

    def create(self):  # noqa
        """Создаёт базу данных."""
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        self.database.Base.metadata.create_all()

    def exists(self):  # noqa
        """Проверяет наличие базы данных по пути в конфигурации."""
        return Path(wacfg.Config.DB_PATH + wacfg.Config.DB_NAME).exists()
