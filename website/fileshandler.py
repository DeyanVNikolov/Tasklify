import datetime
import os
import time
import uuid
from os.path import join, dirname, realpath

import requests
from dateutil import parser
from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import abort
from flask import current_app as app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename, send_from_directory

from website import CAPTCHA1
from . import db
from .mailsender import sendregisterationemail
from .models import Task
from .models import Worker, Boss
from .translator import getword

fileshandler = Blueprint('fileshandler', __name__)

homepage = "views.home"
workerspage = "views.workers"
oneworkerpage = "views.worker"

global csrfg


class StatusDenied(Exception):
    print("StatusDenied Exception")


def checkmaintenance():
    # Not in use
    pass


@fileshandler.errorhandler(StatusDenied)
def redirect_on_status_denied(error):
    print(error)
    return render_template("maintenance.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie)), 403


@fileshandler.route('/uploaded_file/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    checkmaintenance()

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if not current_user.is_authenticated:
        flash(getword("youneedtobeloggedin", cookie), category="error")
        return redirect(url_for('auth.login'))

    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        if current_user.accounttype == "worker":
            imageid = filename.split("_")[0]

            # check if imageid is either workerid or bossid
            worker = Worker.query.filter_by(id=imageid).first()
            if worker is None:
                boss = Boss.query.filter_by(id=imageid).first()
                if boss is None:
                    return redirect(url_for(homepage))
                else:
                    if current_user.boss_id != boss.id:
                        return redirect(url_for(homepage))
            else:
                if worker.id != current_user.id:
                    return redirect(url_for(homepage))
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)


        elif current_user.accounttype == "boss":
            imageid = filename.split("_")[0]
            if Boss.query.filter_by(id=imageid).first() is not None:
                if Boss.query.filter_by(id=imageid).first().id == current_user.id:
                    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)
            elif Worker.query.filter_by(id=imageid).first() is not None:
                if Worker.query.filter_by(id=imageid).first().boss_id == current_user.id:
                    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)

            flash(getword("nopermtoviewthisview", cookie), category="error")
            return redirect(url_for(homepage))

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)


@fileshandler.route("/ugc/uploads/<filename>", methods=["GET"])
def get_file(filename):
    return redirect(url_for('fileshandler.uploaded_file', filename=filename))


def hastebin(text):
    r = requests.post("https://hastebin.com/documents", data=text)
    return "https://hastebin.com/raw/" + r.json()["key"]

@fileshandler.route("/files/<path:id>", methods=["GET", "POST"])
def files(id):
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.accounttype == "worker":
        if current_user.id != id:
            flash(getword("workernotfound", cookie), category="error")
            return redirect(url_for(homepage))
    elif current_user.accounttype == "boss":
        if current_user.id != id:
            if Worker.query.filter_by(id=id).first().boss_id != current_user.id:
                flash(getword("workernotfound", cookie), category="error")
                return redirect(url_for(homepage))

    # check static/uploads for files starting with id
    files = {}
    splitnames = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        # split by _
        file1 = file.split("_")
        if str(file1[0]) == str(id):
            files[file] = file1[1]
    if request.method == "POST":
        if request.form.get("typeform") == "delete":
            file = request.form.get("file")
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
            except Exception as e:
                print(e)
                flash(getword("error", cookie), category="error")
                return redirect(url_for("fileshandler.files", id=id))
            return redirect(url_for("fileshandler.files", id=id))

    return render_template("files.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie),
                           signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie),
                           workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie),
                           logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie),
                           user=current_user, files=files, splitnames=splitnames, delete=getword("delete", cookie))
