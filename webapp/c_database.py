
from pathlib import Path

from flask import Flask  # noqa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from webapp import c_config as wacfg
from webapp import c_models as wamod


class CDatabaseManager:
    """Класс для работы с БД."""

    def __init__(self):
        self.session = None
        self.engine = None
        self.connect()
        if not self.exists():

            self.create()

    def connect(self):
        """Устанавливает соединение с БД."""
        self.engine = create_engine(wacfg.Config.SQLALCHEMY_DATABASE_URI,
                                    echo=wacfg.Config.ALCHEMY_ECHO,
                                    connect_args={'check_same_thread': False})
        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        self.session = session_maker()
        wamod.Base.metadata.bind = self.engine

    def create(self):  # noqa
        """Создаёт базу данных."""
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        wamod.Base.metadata.create_all(wamod.Base.metadata.bind)

    def exists(self):  # noqa
        """Проверяет наличие базы данных по пути в конфигурации."""
        return Path(wacfg.Config.DB_PATH + wacfg.Config.DB_NAME).exists()
