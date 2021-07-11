'''
@File    ：models.py
@Author  ：Bell_Meng
@Date    ：2021/7/10 9:43 
'''

import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    user = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # pastes = db.relationship('PasteBin', backref='user')
    avatar = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User: %s>' % self.name


class ExpirationTime(enum.Enum):
    Never = "从不"
    BurnAfterRead = "阅后即焚"
    TenMinutesAfter = "10分钟后"
    OneHourAfter = "1小时后"
    OneDayAfter = "1天后"
    OneWeekAfter = "1周后"
    TwoWeeksAfter = "2周后"
    OneMonthAfter = "1个月后"
    SixMonthAfter = "6个月后"
    OneYearAfter = "1年后"


class AccessRights(enum.Enum):
    Public = '公开'
    UnListed = '公开不展示'
    Private = '私人'


class CodeType(enum.Enum):
    Text = 'txt'
    MarkDown = 'md'
    Css = 'css'
    JavaScript = 'js'
    Python = 'py'
    Java = 'java'

class PasteBin(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    content = db.Column(db.Text)
    title = db.Column(db.String(128))
    is_highlight = db.Column(db.Enum(CodeType), default='Text')
    access = db.Column(db.Enum(AccessRights))
    access_password = db.Column(db.String(20))
    expiration = db.Column(db.Enum(ExpirationTime))
    never_expiration = db.Column(db.Boolean)
    view_time = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_burn = db.Column(db.Boolean, default=False)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
            if key == "paste_bin_id":
                setattr(self, 'id', value)
