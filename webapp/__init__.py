# -*- coding: utf-8 -*-
"""Модуль пакета веб-приложения."""
# *** Pathlib нужна для определения, существует ли уже БД
from pathlib import Path

# *** Flask
from flask import Flask  # noqa
from flask_sqlalchemy import SQLAlchemy  # noqa

# *** Конфиг приложения
from webapp import c_config as wacfg

# *** Bootstrap пока подождёт
# from flask_bootstrap import Bootstrap4

# *** Создадим экземпляр приложения
application: Flask = Flask(__name__)
application.config.from_object(wacfg.Config)
# bootstrap = Bootstrap4(application)

# *** Создаем объект базы данных
database = SQLAlchemy()
database.init_app(application)

# *** Если БД ещё не создана...
if not Path(wacfg.Config.DB_PATH + wacfg.Config.DB_NAME).exists():

    # *** Создаём её
    with application.app_context():

        database.create_all()

# *** Нужно ли логирование?
if not application.debug:

    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler(wacfg.Config.LOGS_PATH, 'a', wacfg.Config.LOG_SIZE, 10)
    file_handler.setFormatter(logging.Formatter(wacfg.Config.FORMATSTR))
    application.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    application.logger.addHandler(file_handler)
    application.logger.info(f'{wacfg.Config.APPLICATION_NAME} started...')

# *** Включаем остальные модули приложения
from webapp import c_constants as waconst  # noqa: E402,F401
from webapp import c_index as waidx  # noqa: E402,F401
from webapp import c_models as wamdl  # noqa: E402,F401
