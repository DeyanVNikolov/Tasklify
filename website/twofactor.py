from flask import Blueprint

from website import db
from twilio.rest import Client
import os
import pyqrcode
from dotenv import load_dotenv
from .models import Worker, Boss
from flask_sqlalchemy import SQLAlchemy

load_dotenv(".env")

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")


def generate_qr_code(uri, uuid):
    qr = pyqrcode.create(uri)
    qr.png(f"static/qr/{uuid}{uuid}{uuid}.png", scale=6)


def generate_new_factor(user, uuid, id):
    client = Client(account_sid, auth_token)

    print("--------------------")
    print(user)
    print(uuid)
    print(id)
    print("--------------------")

    new_factor = client.verify.v2.services("VA0cc6fbc2e91664f198db098a5475255b").entities(uuid).new_factors.create(
        friendly_name=f"{user}", factor_type='totp')
    generate_qr_code(new_factor.binding['uri'], uuid)

    user = Worker.query.filter_by(id=id).first()
    if user is None:
        user = Boss.query.filter_by(id=id).first()
        if user is None:
            return "403"

    print(user.accounttype)

    return new_factor


def verifyfactor(id, uuid, code):
    client = Client(account_sid, auth_token)

    user = Worker.query.filter_by(id=id).first()
    if user is None:
        user = Boss.query.filter_by(id=id).first()
        if user is None:
            return "403"

    factor = user.factor

    id1 = id
    uuid1 = uuid
    code1 = str(code)
    factor1 = factor

    print("--------------------")
    print(id1)
    print(uuid1)
    print(code1)
    print(factor1)
    print("--------------------")

    verifiedfactor = client.verify.v2.services('VA0cc6fbc2e91664f198db098a5475255b').entities(f'{uuid1}').factors(
        f'{factor1}').update(auth_payload=f'{code1}')

    return verifiedfactor


def verifyuser(id, uuid, code):
    client = Client(account_sid, auth_token)

    user = Worker.query.filter_by(id=id).first()
    if user is None:
        user = Boss.query.filter_by(id=id).first()
        if user is None:
            return "403"

    factor = user.factor

    challenge = client.verify.v2.services('VA0cc6fbc2e91664f198db098a5475255b').entities(f'{uuid}').challenges.create(
        auth_payload=f'{code}', factor_sid=f'{factor}')

    return challenge
