# -*- coding: utf-8 -*-

import os


class Config:
    # *** Название приложения
    APPLICATION_NAME: str = "PyMemorium"
    # *** На каком порту приложение будет работать
    PORT: int = 7777
    # *** Версия приложения
    APPLICATION_REVISION: str = "0.0"
    # *** Естественно, секретный ключ
    SECRET_KEY = os.urandom(24)
    # *** Выводить ли тексты запросов при работе Алхимии?
    ALCHEMY_ECHO: int = 1
    # *** Параметры БД
    DB_PATH: str = "D:\\home\\YandexDisk\\Private\\app_data\\PyMemorium\\"
    DB_NAME: str = "pymemorium.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}{DB_NAME}"
    # *** Параметры логов
    LOG_SIZE: int = 1024 * 1024
    LOGS_PATH: str = "D:\\home\\projects\\pymemorium\\logs\\main.log"
    FORMATSTR: str = ("%(asctime)s %(levelname)s: "
                      "%(message)s [in %(pathname)s:%(lineno)d]")
    # SOURCE_PATH = "/home/template/Dropbox/notebook"
