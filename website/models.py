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

    def __repr__(self):
        return '<Task %r>' % self.id



class Worker(db.Model, UserMixin):
    # string with utf-8 encoding
    id = db.Column(db.String(150), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    accounttype = db.Column(db.String(150))
    registrationid = db.Column(db.String(150))
    boss_id = db.Column(db.String(150), db.ForeignKey('boss.id'))
    tasks = db.relationship('Task')
    plan = db.Column(db.String(150))


class Boss(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    additionalpermissions = db.Column(db.String(150))
    accounttype = db.Column(db.String(150))
    workers = db.relationship('Worker')
    tasks = db.relationship('Task')
    plan = db.Column(db.String(150))
