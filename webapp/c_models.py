# -*- coding: utf-8 -*-
"""Модуль классов моделей таблиц БД."""

from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, \
                       DateTime, Text, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from webapp import c_constants as waconst

# *** Шаблоны именования ключей, индексов и т.п.
convention = {"all_column_names": lambda constraint,
              table: "_".join([column.name for column in constraint.columns.values()]),
              "ix": "ix__%(table_name)s__%(all_column_names)s",
              "uq": "uq__%(table_name)s__%(all_column_names)s",
              "cq": "cq__%(table_name)s__%(constraint_name)s",
              "fk": ("fk__%(table_name)s__%(all_column_names)s__"
                     "%(referred_table_name)s"),
              "pk": "pk__%(table_name)s"
              }

meta_data = MetaData(naming_convention=convention)
Base = declarative_base(metadata=meta_data)


class CAncestor(Base):  # noqa
    """Класс-предок всех классов-таблиц Alchemy."""
    __abstract__ = True
    id = Column(Integer(),
                primary_key=True,
                autoincrement=True,
                nullable=False,
                unique=True)
    fstatus = Column(Integer(),
                     default=waconst.DB_STATUS_ACTIVE)
    fcreated = Column(DateTime(),
                      default=datetime.now)
    fupdated = Column(DateTime(),
                      default=datetime.now,
                      onupdate=datetime.now)

    def __init__(self):
        """Конструктор."""

    def __repr__(self):
        return f"""ID:{self.id},
                   Status:{self.fstatus},
                   Created:{self.fcreated},
                   Updated:{self.fupdated}"""

    @property
    def serialize(self):
        return {
            'id': self.id,
            'fstatus': self.fstatus,
            'created': self.fcreated,
            'updated': self.fupdated
        }


class CFather(CAncestor):
    """Класс - предок моделей таблиц хранения и основной таблицы."""
    __abstract__ = True
    fname = Column(String(64), nullable=False, index=True)

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
    fcontent = Column(Text(), nullable=False)

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
    flink = Column(String(1024), nullable=False)

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
    fpath = Column(String(1024), nullable=False)

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


class CDocument(CFather):
    """Класс модели таблицы для хранения ссылок на локальные документы."""
    __tablename__ = 'tbl_documents'
    fdocument = Column(String(512), nullable=False)
    ffolder = Column(Integer(), ForeignKey('tbl_folders.id'), nullable=False)
    ffolderobj = relationship("CFolder", foreign_keys=[ffolder])
    fdescription = Column(String(512), default="")

    def __init__(self, pname, pdocument, pfolder, pdescription):
        """Конструктор."""
        super().__init__(pname)
        self.fdocument = pdocument
        self.ffolder = pfolder
        self.fdescription = pdescription

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Document:{self.fdocument}
                   Folder:{self.ffolder}
                   Description:{self.fdescription}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["fdocument"] = self.fdocument
        return ancestor_serialize


class CStorage(CFather):
    """Класс модели таблицы хранилища."""

    __tablename__ = 'tbl_storage'
    fnote = Column(Integer(), ForeignKey('tbl_notes.id'), nullable=True)
    fnoteobj = relationship("CNote", foreign_keys=[fnote])
    fweblink = Column(Integer(), ForeignKey('tbl_weblinks.id'), nullable=True)
    fweblinkobj = relationship("CWebLink", foreign_keys=[fweblink])
    fdocument = Column(Integer(), ForeignKey('tbl_documents.id'), nullable=True)
    fdocumentobj = relationship("CDocument", foreign_keys=[fdocument])

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
                   Note:{self.fnote},
                   Weblink:{self.fweblink},
                   Document:{self.fdocument}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["fnote"] = self.fnote
        ancestor_serialize["fweblink"] = self.fweblink
        ancestor_serialize["fdocument"] = self.fdocument
        return ancestor_serialize


class CTagLink(CAncestor):
    """Класс модели таблицы связок основной таблицы с таблицей тегов."""
    __tablename__ = 'tbl_taglinks'
    ftag = Column(Integer(), ForeignKey('tbl_tags.id'), nullable=False)
    frecord = Column(Integer(), ForeignKey('tbl_storage.id'), nullable=False)

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
