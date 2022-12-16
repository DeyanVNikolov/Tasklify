import datetime
import os
import time
import uuid
from os.path import join, dirname, realpath

import requests
from dateutil import parser
from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask import abort
from flask import current_app as app
from flask_wtf.csrf import CSRFProtect
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename, send_from_directory

from website import CAPTCHA1
from . import db
from .mailsender import sendregisterationemail, sendregisterationemailboss
from .models import Task
from .models import Worker, Boss
from .translator import getword
from .addtabs import addtabs
from .fileshandler import fileshandler
externalcallback = Blueprint('externalcallback', __name__)
check_url = "https://oauth2.googleapis.com/tokeninfo?id_token="


@externalcallback.route('/googlecallback', methods=['GET', 'POST'])
def googlelogin():
    if request.method == 'POST':
        csrf_token_cookie = request.cookies.get('g_csrf_token')
        if not csrf_token_cookie:
            abort(403)
        csrf_token_body = request.form.get('g_csrf_token')
        if not csrf_token_body:
            abort(403)
        if csrf_token_cookie != csrf_token_body:
            abort(403)

        credentials = request.form.get('credential')
        if not credentials:
            abort(403)

        response = requests.get(check_url + credentials)
        if response.status_code != 200:
            abort(403)

        data = response.json()
        if data['aud'] != app.config['GOOGLE_CLIENT_ID']:
            abort(403)

        email = data['email']
        if not email:
            abort(403)

        email_verified = data['email_verified']
        if not email_verified:
            abort(403)

        exp = data['exp']
        if not exp:
            abort(403)

        # check if exp is in the past
        if float(exp) < time.time():
            abort(403)

        iss = data['iss']
        if not iss:
            abort(403)

        if iss != "accounts.google.com" and iss != "https://accounts.google.com":
            abort(403)

        sub = data['sub']
        if not sub:
            abort(403)

        user = Worker.query.filter_by(email=email).first()
        if not user:
            user = Boss.query.filter_by(email=email).first()
            if not user:
                return redirect(url_for('auth.sign_up'))

        login_user(user, remember=True)
        return redirect(url_for('views.home'))

    return redirect(url_for('auth.login'))

@externalcallback.route('/googlesignup', methods=['GET', 'POST'])
def googlesignup():
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if request.method == 'POST':
        if request.form.get('emailtogive') is not None and request.form.get('emailtogive') != '' and request.form.get('nametogive') != '' and request.form.get('nametogive') is not None:
            email = request.form.get('emailtogive')
            name = request.form.get('nametogive')
            accounttype = request.form.get('accounttype')
            password = request.form.get('passwordtogive')

            if accounttype == 'worker':
                key = uuid.uuid4().hex[:12]
                new_user = Worker(email=email, first_name=name,
                                  password=generate_password_hash(password, method='sha256'), accounttype="worker",
                                  registrationid=key)
            elif accounttype == 'boss':
                new_user = Boss(email=email, first_name=name,
                                password=generate_password_hash(password, method='sha256'), accounttype="boss")
            else:
                flash("Error. Type not selected.", category='error')
                return redirect(url_for('auth.sign_up'))

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(getword("accountcreated", cookie), category='success')
            if accounttype == 'worker':
                sendregisterationemail(email, name, current_user.registrationid)
                return redirect(url_for('views.boss'))
            else:
                sendregisterationemailboss(email, name)
                return redirect(url_for('views.home'))

        else:
            csrf_token_cookie = request.cookies.get('g_csrf_token')
            if not csrf_token_cookie:
                abort(403)
            csrf_token_body = request.form.get('g_csrf_token')
            if not csrf_token_body:
                abort(403)
            if csrf_token_cookie != csrf_token_body:
                abort(403)

    credentials = request.form.get('credential')
    if not credentials:
        abort(403)

    response = requests.get(check_url + credentials)
    if response.status_code != 200:
        abort(403)

    data = response.json()
    if data['aud'] != app.config['GOOGLE_CLIENT_ID']:
        abort(403)

    email = data['email']
    if not email:
        abort(403)

    email_verified = data['email_verified']
    if not email_verified:
        abort(403)

    exp = data['exp']
    if not exp:
        abort(403)

    # check if exp is in the past
    if float(exp) < time.time():
        abort(403)

    iss = data['iss']
    if not iss:
        abort(403)

    if iss != "accounts.google.com" and iss != "https://accounts.google.com":
        abort(403)

    sub = data['sub']
    if not sub:
        abort(403)

    name = data['name']
    if not name:
        abort(403)

    # check email is not already in use
    user = Worker.query.filter_by(email=email).first()
    if user:
        flash(getword("emailalreadyexists", cookie), category='error')
        return redirect(url_for('auth.sign_up'))
    user = Boss.query.filter_by(email=email).first()
    if user:
        flash(getword("emailalreadyexists", cookie), category='error')
        return redirect(url_for('auth.sign_up'))


    return render_template("googlesignup.html", user=current_user, worker=getword("worker", cookie), boss=getword("boss", cookie), emailrequest=email, namerequest=name, enterpassword=getword("enterpassword", cookie))

@externalcallback.route('/githubcallback', methods=['GET', 'POST'])
def githublogin():

    return redirect("https://github.com/login/oauth/authorize?client_id=dc8fa02eeecfcf3f8ae2")