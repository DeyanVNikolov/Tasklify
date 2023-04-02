import random

from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Sequence
from sqlalchemy.dialects.postgresql import UUID
from . import db
import uuid
import datetime
import sqlalchemy.dialects.postgresql as postgresql
import time

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    task = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.String(100), default=False)
    worker_id = db.Column(db.String(150), db.ForeignKey('worker.id'))
    boss_id = db.Column(db.String(150), db.ForeignKey('boss.id'))
    ordernumber = db.Column(db.Integer)
    actual_id = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(100))
    datedue = db.Column(db.DateTime, default=datetime.datetime.now())
    notified = db.Column(db.Boolean, default=False)
    archive = db.Column(db.Boolean, default=False)
    attachments = db.Column(db.String(1000), default="")

    def __repr__(self):
        return '<Task %r>' % self.id

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != "actual_id" and c.name != "ordernumber" and c.name != "notified"}


class Worker(db.Model, UserMixin):
    # string with utf-8 encoding
    id = db.Column(db.String(150), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    number = db.Column(db.Integer, default=lambda : int(time.time()) + random.randint(100000, 999999), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    accounttype = db.Column(db.String(150))
    registrationid = db.Column(db.String(150))
    boss_id = db.Column(db.String(150), db.ForeignKey('boss.id'))
    tasks = db.relationship('Task')
    plan = db.Column(db.String(150))
    token = db.Column(db.String(150), default=lambda: str(uuid.uuid4().hex), unique=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != "password" and c.name != "token" and c.name != "plan"}


class Boss(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    number = db.Column(db.Integer, default=lambda : int(time.time()) + random.randint(100000, 999999), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    additionalpermissions = db.Column(db.String(150))
    accounttype = db.Column(db.String(150))
    workers = db.relationship('Worker')
    tasks = db.relationship('Task')
    plan = db.Column(db.String(150))
    token = db.Column(db.String(150), default=lambda: str(uuid.uuid4().hex), unique=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != "password" and c.name != "token" and c.name != "plan"}



class Message(db.Model):
    idmessage = db.Column(db.Integer, primary_key=True)
    chat = db.Column(db.Integer, db.ForeignKey('chat.id'))
    id_sender = db.Column(db.String(150))
    id_receiver = db.Column(db.String(150))
    message = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    readdate = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_creator = db.Column(db.String(150))
    name_creator = db.Column(db.String(150))
    id_participant = db.Column(db.String(150))
    name_participant = db.Column(db.String(150))
    messages = db.relationship('Message')



