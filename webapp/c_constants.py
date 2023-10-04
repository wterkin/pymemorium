# -*- coding: utf-8 -*-
"""Модуль с глобальными константами."""
DB_STATUS_DELETED: int = 0
DB_STATUS_ACTIVE: int = 1
DB_NOTE_TYPE: int = 1
DB_DOCUMENT_TYPE: int = 2
DB_WEBLINK_TYPE: int = 3

DB_NAME_SIZE: int = 64

PAGER_FRAMESIZE = 10
PAGER_PAGESIZE = 25

INDEX_PAGE_URL: str = "/index"
INDEX_PAGE: str = "index.html"

# *** Константы сессии.
SESSION_APPLICATION_NAME: str = "appname"
SESSION_IDX_FILTER_STATE: str = "idx_filter_state"
SESSION_IDX_TRASH_STATE: str = "idx_trash_state"
SESSION_IDX_PAGE_NUMBER: str = "idx_page_number"
SESSION_IDX_FRAME_NUMBER: str = "idx_frame_number"


INDEX_FORM_FIRST_FRAME_BUTTON: str = "idx_pager_first_frame"
INDEX_FORM_PREV_FRAME_BUTTON: str = "idx_pager_prev_frame"
INDEX_FORM_NEXT_FRAME_BUTTON: str = "idx_pager_next_frame"
INDEX_FORM_LAST_FRAME_BUTTON: str = "idx_pager_last_frame"