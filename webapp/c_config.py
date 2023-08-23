# -*- coding: utf-8 -*-


import os


class Config():

    APPLICATION_NAME: str = "PyMemorium"
    PORT: int = 7777
    PROGRAM_VERSION: str = "0.11"
    SECRET_KEY = os.urandom(24)
    LOGS_PATH: str = "D:\\home\\projects\\pymemorium\\logs\\main.log"
    # SOURCE_PATH = "/home/template/Dropbox/notebook"
    ALCHEMY_ECHO: int = 1
    DB_PATH: str = "D:\\home\\YandexDisk\\Private\\app_data\\PyMemorium\\"
    DB_NAME: str = "pymemorium.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}{DB_NAME}"
    FORMATSTR: str = ("%(asctime)s %(levelname)s: "
                      "%(message)s [in %(pathname)s:%(lineno)d]")
    LOG_SIZE: int = 1024 * 1024