# -*- coding: utf-8 -*-
"""Модуль роутинга главной страницы. """  # noqa

from flask import render_template
from flask import request
from flask import session
# from flask import redirect
# from flask import url_for

from webapp import application
from webapp import c_constants as waconst
from webapp import db_manager
from webapp import c_models as wamod
# from webapp import c_config as wacfg

GRID_COLUMNS = [["ID", "id", 1, False, 0],
                ["", "", 0, True, 7],
                ["Всего", "ftotalcount", 2, True, 3],
                ["Совм. с учёбой", "fcomblearning", 2, True, 8],
                ["Совм. с восп. детей", "fcombparenting", 2, True, 10],
                ["Женщин с детьми", "fwomanwithchildren", 2, True, 7],
                ["Мат. помощь при рожд. ребёнка", "fchildbirth", 2, True, 16],
                ["Инд. график", "findividualschedule", 2, True, 6],
                ["Дети дошк. возр.", "fshortenedweek", 2, True, 8],
                ["Дети до 14 лет", "fvacationpriorityright", 2, True, 7],
                ["Возм. обуч.", "flearningopportunity", 2, True, 6],
                ["Иные причины-1", "fotherdescription1", 0, True, 8],
                ["Кол-во", "fothervalue1", 2, True, 3],
                ["Иные причины-2", "fotherdescription2", 0, True, 8],
                ["Кол-во", "fothervalue2", 2, True, 3]
                ]

ALIGNS = ("align_left", "align_center", "align_right")


def main_query():
    """Возвращает выборку данных в соответствии с установками."""
    query = db_manager.session.query(wamod.CStorage)
    # query = query.outerjoin(wamod.CTagLink, wamod.CTagLink.frecord == wamod.CStorage.id)
    # query = query.join(wamod.CTag, wamod.CTagLink.ftag == wamod.CTag.id)
    # , wamod.CTagLink, wamod.CTag
    result = query.all()
    for item in result:

        if item.fweblink is not None:

            print(item.fweblinkobj)
        if item.fdocument is not None:

            print(item.fdocumentobj)
        if item.fnote is not None:

            print(item.fnoteobj)
    # print(query.one().fdocumentobj)

        # print()


def index_get():
    """Обработчик запросов GET."""
    print("* IDX:GET *")
    session[waconst.SESSION_IDX_FILTER_STATE] = False
    main_query()
    # print(session[waconst.SESSION_IDX_FILTER_STATE])
    return render_template(waconst.INDEX_PAGE)


def index_post():
    """Обработчик запросов POST."""
    print("* IDX:POST *")
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
