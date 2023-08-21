

# 1. Справочник тэгов
# 2. Справочник типов материалов - заметка, ссылка, файл
# 3. Главная таблица, в которой будут связаны тэги, типы и ...
# Подумаем.
# class CTypes(CAncestor):
# class CTags(CAncestor):
# class CTagLinks(CAncestor):
# class CNotes(CAncestor):
# class CLinks(CAncestor):
# class CFolder(CAncestor)
# class CDocuments(CAncestor):
# class CMaster(CAncestor):

from datetime import datetime

# from _ctypes import CFuncPtr
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from webapp import c_config as wacfg

# 'sqlite:///'+self.config.restore_value(c_config.DATABASE_FILE_KEY)

from webapp import c_constants as waconst

database: SQLAlchemy


def initialize_database(papplication: Flask):
    """Создаёт экземпляр класса SQLAlchemy."""

    global database
    database = SQLAlchemy(papplication)


class CAncestor(database.Model):  # noqa
    """Класс-предок всех классов-таблиц Alchemy."""
    __abstract__ = True
    id = database.Column(database.Integer(),
                         primary_key=True,
                         autoincrement=True,
                         nullable=False,
                         unique=True)
    fstatus = database.Column(database.Integer(),
                              default=waconst.DB_STATUS_ACTIVE)
    fcreated = database.Column(database.DateTime(),
                               default=datetime.now)
    fupdated = database.Column(database.DateTime(),
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
    fname = database.Column(database.String(64), nullable=False, index=True)

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
    fcontent = database.Column(database.Text(), nullable=False)

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
    flink = database.Column(database.String(1024), nullable=False)

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
    fpath = database.Column(database.String(1024), nullable=False)

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
    fdocument = database.Column(database.String(512), nullable=False)
    ffolder = database.Column(database.Integer(), database.ForeignKey('tbl_folders.id'), nullable=False)

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

    ftype = database.Column(database.Integer(), database.ForeignKey('tbl_types.id'))
    fnote = database.Column(database.Integer(), database.ForeignKey('tbl_notes.id'), nullable=True)
    fweblink = database.Column(database.Integer(), database.ForeignKey('tbl_weblinks.id'), nullable=True)
    fdocument = database.Column(database.Integer(), database.ForeignKey('tbl_documents.id'), nullable=True)

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

# class CTagLinks(CAncestor):
#     """Класс таблицы связок основной таблицы с таблицей тегов."""
"""
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, update=datetime.utcnow)

    def __repr__(self):
    return "<{}:{}>".format(self.id,  self.title[:10])
"""