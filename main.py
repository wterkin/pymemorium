# -*- coding: utf-8 -*-
"""Запускающий модуль приложения."""

from webapp import application
from webapp import c_config as wacfg


if __name__ == '__main__':

    print(f"***** {wacfg.Config.APPLICATION_NAME}, редакция от {wacfg.Config.APPLICATION_REVISION} Serving on {wacfg.Config.APPLICATION_PORT} ...")
    application.run(host=wacfg.Config.APPLICATION_HOST, port=wacfg.Config.APPLICATION_PORT, debug=wacfg.Config.APPLICATION_DEBUG)
