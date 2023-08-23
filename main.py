# -*- coding: utf-8 -*-
"""Запускающий модуль приложения."""

from webapp import application
from webapp import c_config as wacfg


if __name__ == '__main__':

    print(f"***** {wacfg.Config.APPLICATION_NAME}, редакция от {wacfg.Config.APPLICATION_REVISION} Serving on {wacfg.Config.PORT} ...")
    application.run(host='127.0.0.1', port=wacfg.Config.PORT, debug=True)
