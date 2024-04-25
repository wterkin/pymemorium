# -*- coding: utf-8 -*-
"""Модуль конфигурации приложения."""
import os


class Config:
    # *** Название приложения
    APPLICATION_NAME: str = "PyMemorium"
    # *** На каком IP приложение будет отвечать?
    APPLICATION_HOST: str = '127.0.0.1'
    # *** На каком порту приложение будет работать?
    APPLICATION_PORT: int = 7777
    # *** Версия приложения
    APPLICATION_REVISION: str = "0.0"
    # *** Флаг отладки
    APPLICATION_DEBUG: bool = True
    # *** Естественно, секретный ключ
    SECRET_KEY: str = os.urandom(24)
    # *** Выводить ли тексты запросов при работе Алхимии?
    ALCHEMY_ECHO: int = 0
    # *** Параметры БД
    DB_PATH: str = "./"
    DB_NAME: str = "pymemorium.db"
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{DB_PATH}{DB_NAME}"
    # *** Параметры логов
    LOG_SIZE: int = 1024 * 1024
    LOGS_PATH: str = "./logs\\main.log"
    FORMATSTR: str = ("%(asctime)s %(levelname)s: "
                      "%(message)s [in %(pathname)s:%(lineno)d]")
    # SOURCE_PATH = "/home/template/Dropbox/notebook"
    DOCUMENTS_PATH: str = "./documentation/"
