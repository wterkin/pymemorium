from flask_sqlalchemy import SQLAlchemy
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
from webapp import c_config as wacfg

# 'sqlite:///'+self.config.restore_value(c_config.DATABASE_FILE_KEY)


database: object


class CAncestor(database.Model):
    """Класс-предок всех классов-таблиц Alchemy."""
    __abstract__ = True
    id = database.Column(database.Integer,
                         primary_key=True,
                         autoincrement=True,
                         nullable=False,
                         unique=True)
    fstatus = database.Column(database.Integer,
                              nullable=False,
                              )

    def __init__(self, pstatus):
        """Конструктор."""
        self.fstatus = pstatus

    def __repr__(self):
        return f"""ID:{self.id},
                   Status:{self.fstatus}"""


class CTypes(CAncestor):
    __tablename__ = 'tbl_types'
    fname = database.Column(database.String(64), nullable=False)

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Name:{self.fname}"""


class CTags(CAncestor):
    __tablename__ = 'tbl_tags'
    fname = database.Column(database.String(64), nullable=False)


    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Name:{self.fname}"""

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