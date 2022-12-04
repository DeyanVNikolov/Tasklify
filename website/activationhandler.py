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
from .addtabs import addtabs
from .fileshandler import fileshandler

activationhandler = Blueprint('activationhandler', __name__)

homepage = "views.home"
workerspage = "views.workers"
oneworkerpage = "views.worker"

global csrfg



@activationhandler.route("/activate/<path:id>", methods=["GET", "POST"])
def activate(id):
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if not current_user.is_authenticated:
        return redirect(url_for(homepage))

    if current_user.accounttype != "boss":
        return redirect(url_for(homepage))

    worker = Worker.query.filter_by(registrationid=id).first()
    if worker is None:
        flash(getword("workernotfound", cookie), category="error")
        return redirect(url_for(homepage))

    if worker.boss_id is not None:
        flash(getword("workernotfound", cookie), category="error")
        return redirect(url_for(homepage))

    if request.method == 'POST':
        if request.form.get("typeform") == "activate":
            try:
                if worker is None:
                    flash(getword("workernotfound", cookie), category="error")
                    return redirect(url_for(homepage))

                if worker.boss_id is None or worker.boss_id == "" or worker.boss_id == 0:
                    worker.boss_id = current_user.id
                    db.session.commit()
                    flash(getword("workeradded", cookie), category="success")
                    return redirect(url_for(workerspage))
                else:
                    flash(getword("workeralreadyadded", cookie), category="error")
                    return redirect(url_for(homepage))
            except Exception as e:
                flash(str(e), category="error")
                return redirect(url_for(workerspage))

    return render_template("activate.html", user=current_user, activatetext=getword("activatetext", cookie), id=id,
                           activatetext1=getword("activatetext1", cookie), nametext=getword("name", cookie),
                           emailtext=getword("email", cookie), name=worker.first_name, email=worker.email,
                           areyousure=getword("areyousure", cookie), makesuretext=getword("makesuretext1", cookie),
                           submit=getword("submit", cookie))


@activationhandler.route("/a/<path:id>", methods=["GET", "POST"])
def a(id):
    return redirect(url_for("activationhandler.activate", id=id))