# -*- coding: utf-8 -*-
"""Модуль пакета веб-приложения."""
# *** Flask
from flask import Flask  # noqa

# *** Конфиг приложения
from webapp import c_config as wacfg
from webapp import c_database as wadb

# *** Создадим экземпляр приложения
application: Flask = Flask(__name__)
application.config.from_object(wacfg.Config)

# *** Создаем объект менеджера базы данных
db_manager = wadb.CDatabaseManager()

from webapp import c_models as wamod  # noqa: E402,F401

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
