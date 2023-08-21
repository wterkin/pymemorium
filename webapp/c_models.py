# -*- coding: utf-8 -*-
"""Модуль классов моделей таблиц БД."""

from datetime import datetime

# from _ctypes import CFuncPtr
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# from webapp import c_config as wacfg

# 'sqlite:///'+self.config.restore_value(c_config.DATABASE_FILE_KEY)

from webapp import c_constants as waconst
from webapp import c_database as wadb


class CAncestor(wadb.database.Model):  # noqa
    """Класс-предок всех классов-таблиц Alchemy."""
    __abstract__ = True
    id = wadb.database.Column(wadb.database.Integer(),
                              primary_key=True,
                              autoincrement=True,
                              nullable=False,
                              unique=True)
    fstatus = wadb.database.Column(wadb.database.Integer(),
                                   default=waconst.DB_STATUS_ACTIVE)
    fcreated = wadb.database.Column(wadb.database.DateTime(),
                                    default=datetime.now)
    fupdated = wadb.database.Column(wadb.database.DateTime(),
                                    default=datetime.now,
                                    update=datetime.now)

    def __init__(self):
        """Конструктор."""

    def __repr__(self):
        return f"""ID:{self.id},
                   Status:{self.fstatus},
                   Created:{self.fcreated},
                   Updated:{self.updated}"""

    @property
    def serialize(self):
        return {
            'id': self.id,
            'fstatus': self.fstatus,
            'created': self.fcreated,
            'updated': self.fupdated
        }


class CFather(CAncestor):
    """Родительский класс."""
    __abstract__ = True
    fname = wadb.database.Column(wadb.database.String(64), nullable=False, index=True)

    def __init__(self, pname):
        """Конструктор."""
        super().__init__()
        self.fname = pname

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr}
                   Name: {self.fname}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize['fname'] = self.fname
        return ancestor_serialize


class CType(CFather):
    """Класс модели таблицы справочника типов единиц хранения."""
    __tablename__ = 'tbl_types'

    def __init__(self, pname):
        """Конструктор."""
        super().__init__(pname)

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        return ancestor_serialize


class CTag(CFather):
    """Класс модели таблицы справочника тэгов."""
    __tablename__ = 'tbl_tags'

    def __init__(self, pname):
        """Конструктор."""
        super().__init__(pname)

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        return ancestor_serialize


class CNote(CFather):
    """Класс модели таблицы хранения заметок."""
    __tablename__ = 'tbl_notes'
    fcontent = wadb.database.Column(wadb.database.Text(), nullable=False)

    def __init__(self, pname, pcontent):
        """Конструктор."""
        super().__init__(pname)
        self.fcontent = pcontent

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Note:{self.fcontent}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["content"] = self.fcontent
        return ancestor_serialize


class CWebLink(CFather):
    """Класс модели таблицы хранения ссылок на web-ресурсы."""
    __tablename__ = 'tbl_weblinks'
    flink = wadb.database.Column(wadb.database.String(1024), nullable=False)

    def __init__(self, pname, plink):
        """Конструктор."""
        super().__init__(pname)
        self.flink = plink

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Link:{self.flink}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["flink"] = self.flink
        return ancestor_serialize


class CFolder(CFather):
    """Класс модели таблицы путей к папкам хранения документов."""
    __tablename__ = 'tbl_folders'
    fpath = wadb.database.Column(wadb.database.String(1024), nullable=False)

    def __init__(self, pname, ppath):
        """Конструктор."""
        super().__init__(pname)
        self.fpath = ppath

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Path:{self.fpath}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["fpath"] = self.fpath
        return ancestor_serialize


class CDocuments(CFather):
    """Класс модели таблицы для хранения ссылок на локальные документы."""
    __tablename__ = 'tbl_documents'
    fdocument = wadb.database.Column(wadb.database.String(512), nullable=False)
    ffolder = wadb.database.Column(wadb.database.Integer(), wadb.database.ForeignKey('tbl_folders.id'), nullable=False)

    def __init__(self, pname, pdocument):
        """Конструктор."""
        super().__init__(pname)
        self.fdocument = pdocument

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Document:{self.fdocument}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["fdocument"] = self.fdocument
        return ancestor_serialize


class CStorage(CFather):
    """Класс модели таблицы хранилища."""

    ftype = wadb.database.Column(wadb.database.Integer(), wadb.database.ForeignKey('tbl_types.id'))
    fnote = wadb.database.Column(wadb.database.Integer(), wadb.database.ForeignKey('tbl_notes.id'), nullable=True)
    fweblink = wadb.database.Column(wadb.database.Integer(), wadb.database.ForeignKey('tbl_weblinks.id'), nullable=True)
    fdocument = wadb.database.Column(wadb.database.Integer(), wadb.database.ForeignKey('tbl_documents.id'), nullable=True)

    def __init__(self, pname, ptype, pnote, pweblink, pdocument):
        """Конструктор."""
        super().__init__(pname)
        self.ftype = ptype
        self.fnote = pnote
        self.fweblink = pweblink
        self.fdocument = pdocument

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Type:{self.ftype},
                   Note:{self.fnote},
                   Weblink:{self.fweblink},
                   Document:{self.fdocument}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["ftype"] = self.ftype
        ancestor_serialize["fnote"] = self.fnote
        ancestor_serialize["fweblink"] = self.fweblink
        ancestor_serialize["fdocument"] = self.fdocument
        return ancestor_serialize


class CTagLinks(CAncestor):
    """Класс модели таблицы связок основной таблицы с таблицей тегов."""
    ftag = wadb.database.Column(wadb.database.Integer(), wadb.database.ForeignKey('tbl_tags.id'), nullable=False)
    frecord = wadb.database.Column(wadb.database.Integer(), wadb.database.ForeignKey('tbl_storage.id'), nullable=False)

    def __init__(self, ptag, precord):
        """Конструктор."""
        super().__init__()
        self.ftag = ptag
        self.frecord = precord

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Tag:{self.ftag},
                   Record:{self.frecord}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["ftag"] = self.ftag
        ancestor_serialize["frecord"] = self.frecord
        return ancestor_serialize
