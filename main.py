# -*- coding: utf-8 -*-
"""Запускающий модуль приложения."""
import os

# from flask import send_from_directory

from webapp import application
from webapp import c_constants as waconst
from webapp import c_config as wacfg


if __name__ == '__main__':

    print(f"***** {wacfg.Config.APPLICATION_NAME}, редакция от {waconst.PROGRAM_REVISION} Serving on {wacfg.Config.PORT}...")
    application.run(host='127.0.0.1', port=wacfg.Config.PORT, debug=True)
