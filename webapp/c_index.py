# -*- coding: utf-8 -*-
"""Модуль роутинга главной страницы. """  # noqa

from flask import render_template
from flask import request
from flask import session
# from flask import redirect
# from flask import url_for

from webapp import application
from webapp import c_config as wacfg
from webapp import c_constants as waconst
from webapp import c_models as wamod
from webapp import db_manager

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
    data_list: list = []
    query = db_manager.session.query(wamod.CStorage)
    # query = query.outerjoin(wamod.CTagLink, wamod.CTagLink.frecord == wamod.CStorage.id)
    # query = query.join(wamod.CTag, wamod.CTagLink.ftag == wamod.CTag.id)
    # , wamod.CTagLink, wamod.CTag
    result = query.all()
    tags_list: list = []
    for item in result:

        tags: list = []
        tagline: str = " "
        tag_query = db_manager.session.query(wamod.CTagLink)
        tag_query = tag_query.filter(wamod.CTagLink.frecord == item.id)
        tag_query = tag_query.outerjoin(wamod.CTag, wamod.CTagLink.ftag == wamod.CTag.id)
        for tag in tag_query.all():
            tags.append(tag.ftagobj.fname)
        if len(tags) > 0:
            tagline = ", ".join(tags)
        tags_list.append(tagline)
        if item.ftype == waconst.DB_WEBLINK_TYPE:
            print(f"*** {item.fweblinkobj.fname} [{tagline}] ****")

        if item.ftype == waconst.DB_DOCUMENT_TYPE:
            print(f"*** {item.fdocumentobj.fdescription}  [{tagline}] ***")
        if item.ftype == waconst.DB_NOTE_TYPE:
            print(f"*** {item.fnoteobj.fname} [{tagline}] ***")
    return result, tags_list


def update_content():
    """Обновляет выборку данных с новыми параметрами."""
    data_list, tags_list = main_query()
    # param_frames param_part_frame param_part_frame_size param_part_page param_framesize param_pagesize
    # param_records
    frames, part_frame, part_frame_size, part_page, part_page_size = pager_recalc(len(data_list))
    session[waconst.SESSION_IDX_FRAME_NUMBER] = 0
    session[waconst.SESSION_IDX_PAGE_NUMBER] = 0
    return render_template(waconst.INDEX_PAGE,
                           param_data=data_list,
                           param_tags=tags_list,
                           param_delete_record_id=2,
                           param_frames=frames,
                           param_part_frame=part_frame,
                           param_part_frame_size=part_frame_size,
                           param_part_page=part_page,
                           param_part_page_size=part_page_size,
                           param_framesize=waconst.PAGER_FRAMESIZE,
                           param_pagesize=waconst.PAGER_PAGESIZE,
                           param_records=len(data_list)
                           )


def pager_recalc(precords):
    """Процедура производит расчёт параметров пейджера."""
    assert precords is not None, ("Assert: [c_insert:pager_recalc]: No "
                                  "<precords> parameter specified!")

    part_frame_records: int = 0
    part_frame: bool = False
    part_frame_size: int = 0
    part_page: bool = False
    part_page_size: int = 0
    # *** Найдём к-во полных фреймов
    frames: int = (precords // (waconst.PAGER_FRAMESIZE * waconst.PAGER_PAGESIZE))
    full_frames_records: int = (frames * waconst.PAGER_FRAMESIZE * waconst.PAGER_PAGESIZE)
    # *** Если к-во записей не делится нацело на к-во записей во фрейме
    if precords % (waconst.PAGER_PAGESIZE * waconst.PAGER_FRAMESIZE) > 0:
        # *** Добавим неполный фрейм
        part_frame = True
        # *** Посчитаем, сколько записей будет в последнем, неполном фрейме
        part_frame_records = precords - full_frames_records
        # *** Рассчитаем к-во страниц в последнем фрейме
        part_frame_size = int(part_frame_records / waconst.PAGER_PAGESIZE)
    # *** Если к-во зап. в выборке не делится нацело на к-во зап. на странице
    if precords % waconst.PAGER_PAGESIZE > 0:
        # *** Увеличиваем к-во страниц в неполном фрейме на 1
        part_page = True
        # *** Рассчитаем к-во записей на последней странице ???
        part_page_size = (part_frame_records - part_frame_size * waconst.PAGER_PAGESIZE)
    return frames, part_frame, part_frame_size, \
           part_page, part_page_size


def index_get():
    """Обработчик запросов GET."""
    print("* IDX:GET *")
    session[waconst.SESSION_IDX_FILTER_STATE] = False
    session[waconst.SESSION_APPLICATION_NAME] = wacfg.Config.APPLICATION_NAME
    return update_content()


def index_post():
    """Обработчик запросов POST."""
    print("* IDX:POST *")
    return update_content()


@application.route(waconst.INDEX_PAGE_URL, methods=["GET", "POST"])
@application.route("/", methods=["GET", "POST"])
# @wa_prc.login_required
def index():
    """Обработчик запросов GET/POST."""

    if request.method == 'GET':

        return index_get()
    elif request.method == 'POST':

        return index_post()
