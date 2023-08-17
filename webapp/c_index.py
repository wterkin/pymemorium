# -*- coding: utf-8 -*-
"""Модуль роутинга главной страницы. """  # noqa

# from flask import redirect
from flask import render_template
from flask import request
# from flask import session
# from flask import url_for

from webapp import application
# import webapp as waapp
from webapp import c_constants as waconst

INDEX_PAGE = "index.html"


def index_get():
    """Обработчик запросов GET."""
    return render_template(INDEX_PAGE)


def index_post():
    """Обработчик запросов POST."""
    return render_template(INDEX_PAGE)

# waapp.application.route(waconst.INDEX_PAGE_URL, methods=["GET", "POST"])
# waapp.application.route("/", methods=["GET", "POST"])


@application.route(waconst.INDEX_PAGE_URL, methods=["GET", "POST"])
@application.route("/", methods=["GET", "POST"])
# @wa_prc.login_required
def index():
    """Обработчик запросов GET/POST."""

    if request.method == 'GET':

        return index_get()
    elif request.method == 'POST':

        return index_post()
