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


class CTag(CAncestor):
    """Класс модели таблицы справочника тэгов."""
    __tablename__ = 'tbl_tags'
    fname = Column(String(waconst.DB_NAME_SIZE), nullable=False)

    def __init__(self, pname):
        """Конструктор."""
        super().__init__()
        self.fname = pname

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""* Tag *
                   {ancestor_repr},
                   Name: {self.fname}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["name"] = self.fname
        return ancestor_serialize


class CType(CAncestor):
    """Класс модели таблицы справочника типов единиц хранения."""
    __tablename__ = 'tbl_types'
    fname = Column(String(waconst.DB_NAME_SIZE), nullable=False)

    def __init__(self, pname):
        """Конструктор."""
        super().__init__()
        self.fname = pname

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""* CType * 
                   {ancestor_repr},
                   Name: {self.fname}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["name"] = self.fname
        return ancestor_serialize



class CNote(CAncestor):
    """Класс модели таблицы хранения заметок."""
    __tablename__ = 'tbl_notes'
    fname = Column(String(waconst.DB_NAME_SIZE), nullable=False)
    fcontent = Column(Text(), nullable=False)

    def __init__(self, pname, pcontent):
        """Конструктор."""
        super().__init__()
        self.fname = pname
        self.fcontent = pcontent

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""* Note *
                   {ancestor_repr},
                   Name:{self.fname},
                   Content:{self.fcontent}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["name"] = self.fname
        ancestor_serialize["content"] = self.fcontent
        return ancestor_serialize


class CWebLink(CAncestor):
    """Класс модели таблицы хранения ссылок на web-ресурсы."""
    __tablename__ = 'tbl_weblinks'
    fname = Column(String(waconst.DB_NAME_SIZE), nullable=False)
    flink = Column(String(1024), nullable=False)

    def __init__(self, pname, plink):
        """Конструктор."""
        super().__init__()
        self.fname = pname
        self.flink = plink

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""* WebLink *
                   {ancestor_repr},
                   Name:{self.fname},
                   Link:{self.flink}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["name"] = self.fname
        ancestor_serialize["link"] = self.flink
        return ancestor_serialize


class CFolder(CAncestor):
    """Класс модели таблицы путей к папкам хранения документов."""
    __tablename__ = 'tbl_folders'
    fname = Column(String(waconst.DB_NAME_SIZE), nullable=False)
    fpath = Column(String(1024), nullable=False)

    def __init__(self, pname, ppath):
        """Конструктор."""
        super().__init__()
        self.fname = pname
        self.fpath = ppath

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""* Folder *
                   {ancestor_repr},
                   Name:{self.fname},
                   Path:{self.fpath}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["name"] = self.fname
        ancestor_serialize["path"] = self.fpath
        return ancestor_serialize


class CDocument(CAncestor):
    """Класс модели таблицы для хранения ссылок на локальные документы."""
    __tablename__ = 'tbl_documents'
    fdescription = Column(Text(), nullable=False)
    fdocument = Column(String(512), nullable=False)
    ffolder = Column(Integer(), ForeignKey('tbl_folders.id'), nullable=False)
    ffolderobj = relationship("CFolder", foreign_keys=[ffolder])

    def __init__(self, pname, pdocument, pfolder, pdescription):
        """Конструктор."""
        super().__init__()
        self.fdocument = pdocument
        self.ffolder = pfolder
        self.fdescription = pdescription

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""* Document *
                   {ancestor_repr},
                   Document:{self.fdocument}
                   Folder:{self.ffolder}
                   Description:{self.fdescription}"""

    @property
    def serialize(self):
        ancestor_serialize = super().serialize
        ancestor_serialize["document"] = self.fdocument
        ancestor_serialize["folder"] = self.ffolder
        ancestor_serialize["description"] = self.fdescription
        return ancestor_serialize


class CStorage(CAncestor):
    """Класс модели таблицы хранилища."""

    __tablename__ = 'tbl_storage'
    ftype = Column(Integer(), ForeignKey('tbl_types.id'))
    fnote = Column(Integer(), ForeignKey('tbl_notes.id'), nullable=True)
    fnoteobj = relationship("CNote", foreign_keys=[fnote])
    fweblink = Column(Integer(), ForeignKey('tbl_weblinks.id'), nullable=True)
    fweblinkobj = relationship("CWebLink", foreign_keys=[fweblink])
    fdocument = Column(Integer(), ForeignKey('tbl_documents.id'), nullable=True)
    fdocumentobj = relationship("CDocument", foreign_keys=[fdocument])

    def __init__(self, ptype, pnote, pweblink, pdocument):
        """Конструктор."""
        super().__init__()
        self.ftype = ptype
        self.fnote = pnote
        self.fweblink = pweblink
        self.fdocument = pdocument

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Type: {self.ftype},
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


class CTagLink(CAncestor):
    """Класс модели таблицы связок основной таблицы с таблицей тегов."""
    __tablename__ = 'tbl_taglinks'
    ftag = Column(Integer(), ForeignKey('tbl_tags.id'), nullable=False)
    frecord = Column(Integer(), ForeignKey('tbl_storage.id'), nullable=False)
    ftagobj = relationship("CTag", foreign_keys=[ftag])

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
        ancestor_serialize["tag"] = self.ftag
        ancestor_serialize["record"] = self.frecord
        return ancestor_serialize
