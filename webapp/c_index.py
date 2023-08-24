# -*- coding: utf-8 -*-
"""Модуль роутинга главной страницы. """  # noqa

from flask import render_template
from flask import request
from flask import session
# from flask import redirect
# from flask import url_for

from webapp import application
from webapp import c_constants as waconst
from webapp import c_config as wacfg
from webapp import c_models as wamod


def main_query():
    """Возвращает выборку данных в соответствии с установками."""
    query: object = wamod.CStorage


def index_get():
    """Обработчик запросов GET."""
    session["APPLICATION_NAME"] = wacfg.Config.APPLICATION_NAME
    return render_template(waconst.INDEX_PAGE)


def index_post():
    """Обработчик запросов POST."""
    return render_template(waconst.INDEX_PAGE)


@application.route(waconst.INDEX_PAGE_URL, methods=["GET", "POST"])
@application.route("/", methods=["GET", "POST"])
# @wa_prc.login_required
def index():
    """Обработчик запросов GET/POST."""

    if request.method == 'GET':

        return index_get()
    elif request.method == 'POST':

        return index_post()
