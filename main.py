# -*- coding: utf-8 -*-
"""Запускающий модуль приложения."""
import os
from webapp import application
from webapp import c_constants as waconst
# from flask import send_from_directory
from c_config import Config

@application.route('/')
def index():

    return "Hello World"

if __name__ == '__main__':

    print(f"***** {Config.APPLICATION_NAME}, редакция от {waconst.PROGRAM_REVISION} Serving on {Config.PORT}...")
    application.run(host='127.0.0.1', port=Config.PORT, debug=True)
