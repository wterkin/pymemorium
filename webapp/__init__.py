# -*- coding: utf-8 -*-
"""Модуль пакета веб-приложения."""

from webapp import c_config as wacfg
from webapp import c_database as wadb
from flask import Flask  # noqa
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy  # noqa

LOG_SIZE = 1024 * 1024
FORMATSTR = ("%(asctime)s %(levelname)s: "
             "%(message)s [in %(pathname)s:%(lineno)d]")


application = Flask(__name__)
application.config.from_object(wacfg.Config)
bootstrap = Bootstrap4(application)
wadb.database = SQLAlchemy(application)

from webapp import c_constants as waconst   # noqa: E402,F401
from webapp import c_index as waidx  # noqa: E402,F401


if not application.debug:

    import logging

    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler(wacfg.Config.LOGS_PATH, 'a', LOG_SIZE, 10)
    file_handler.setFormatter(logging.Formatter(FORMATSTR))
    application.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    application.logger.addHandler(file_handler)
    application.logger.info(f'{wacfg.Config.APPLICATION_NAME} started...')
