# -*- coding: utf-8 -*-
"""Модуль пакета веб-приложения."""

from flask import Flask  # noqa
from flask_sqlalchemy import SQLAlchemy # noqa

from c_config import Config
import c_database as cdb

LOG_SIZE = 1024 * 1024
FORMATSTR = ("%(asctime)s %(levelname)s: "
             "%(message)s [in %(pathname)s:%(lineno)d]")

application = Flask(__name__)
application.config.from_object(Config)
cdb.database = SQLAlchemy(application)

from webapp import c_constants as waconst # noqa: E402,F401

if not application.debug:

    import logging

    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(Config.LOGS_PATH, 'a', LOG_SIZE, 10)
    file_handler.setFormatter(logging.Formatter(FORMATSTR))
    application.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    application.logger.addHandler(file_handler)
    application.logger.info('PyMemorium started...')
