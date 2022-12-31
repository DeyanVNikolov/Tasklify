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
from .models import Worker, Boss, Chat
from .translator import getword

addtabs = Blueprint('addtabs', __name__)

homepage = "views.home"
workerspage = "views.workers"
oneworkerpage = "views.worker"

global csrfg


class StatusDenied(Exception):
    print("StatusDenied Exception")


def checkmaintenance():
    # Not in use
    pass


@addtabs.errorhandler(StatusDenied)
def redirect_on_status_denied(error):
    print(error)
    return render_template("maintenance.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie)), 403


@addtabs.route("/employ/sign-up", methods=["GET", "POST"])
def employ_signup():

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.accounttype == "worker":
        return redirect(url_for(homepage))

    captcha = CAPTCHA1.create()

    if request.method == 'POST':
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if c_hash is None:
            return render_template("hash_error.html", profilenav=getword("profilenav", cookie),
                                   loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                                   tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                                   adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                                   homenav=getword("homenav", cookie), user=current_user, chatnav=getword("chatnav", cookie))

        if not CAPTCHA1.verify(c_text, c_hash):
            flash(getword("captchawrong", cookie), category='error')
            return redirect(url_for('addtabs.employ_signup'))

        email = request.form.get('email')

        try:
            v = validate_email(email, check_deliverability=True)
            email = v["email"]
            parts1 = email.split('@')
            if parts1[1] == "tasklify.me":
                flash(getword("tasklifymedomainnotallowed", cookie), category='error')
                return redirect(url_for('addtabs.employ_signup'))
        except EmailNotValidError as e:
            flash(str(e), category='error')
            return redirect(url_for('addtabs.employ_signup'))

        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Worker.query.filter_by(email=email).first()
        if not user:
            user = None

        if user:
            flash(getword("emailalreadyexists", cookie), category='error')
        elif len(email) < 4:
            flash(getword("emailtooshort", cookie), category='error')
        elif len(first_name) < 2:
            flash(getword("nametooshort", cookie), category='error')
        elif password1 != password2:
            flash(getword("passwordsdontmatch", cookie), category='error')
        elif len(password1) < 8:
            flash(getword("passwordtooshort", cookie), category='error')
        else:
            key = uuid.uuid4().hex[:12]
            new_user = Worker(email=email, first_name=first_name,
                              password=generate_password_hash(password1, method='sha256'), accounttype="worker",
                              registrationid=key)

            db.session.add(new_user)
            db.session.commit()
            flash(getword("accountcreated", cookie), category='success')
            sendregisterationemail(email, first_name, key)
            return redirect(url_for('views.workers'))

    return render_template("employ_signup.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user, captcha=captcha,
                           emailtext=getword("email", cookie), nametext=getword("name", cookie),
                           passwordtext=getword("password", cookie), passwordconfirm=getword("cnewpassword", cookie),
                           submit=getword("submit", cookie), firstandlast=getword("firstandlast", cookie),
                           signup=getword("signupemploy", cookie), enteremail=getword("enteremail", cookie),
                           alreadyhaveaccount=getword("alreadyhaveaccount", cookie),
                           loginhere=getword("loginhere", cookie),
                           databeingproccessed=getword("databeingproccessed", cookie),
                           employreccode=getword("employreccode", cookie),
                           addemployeeinfosignup=getword("addemployeeinfosignup", cookie),
                           worker=getword("worker", cookie), boss=getword("boss", cookie), goback=getword("goback", cookie), chatnav=getword("chatnav", cookie))


@addtabs.route("/add/employee", methods=["GET", "POST"])
def add_employee():

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.accounttype == "worker":
        return redirect(url_for(homepage))

    if request.method == 'POST':
        if request.form.get("typeform") == "add":
            id = request.form.get('ID')

            if id == "" or id is None:
                flash(getword("missingid", cookie), category="error")
            else:
                worker = Worker.query.filter_by(registrationid=id).first()
                if worker is None:
                    flash(getword("noworkerwithid", cookie), category="error")
                else:
                    if worker.boss_id is None:
                        worker.boss_id = current_user.id
                        newchat = Chat(id_creator=current_user.id, id_participant=worker.id, name_creator=current_user.first_name, name_participant=worker.first_name)
                        db.session.add(newchat)
                        db.session.commit()
                        flash(getword("workeradded", cookie), category="success")
                    else:
                        flash(getword("workeralreadyadded", cookie), category="error")

    return render_template("add_employee.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user,
                           addemployee=getword("addemployee", cookie),
                           addemployeeinfo=getword("addemployeeinfo", cookie), enterid=getword("enterid", cookie),
                           submit=getword("submit", cookie), databeingproccessed=getword("databeingproccessed", cookie),
                           addemployeeinfosignup=getword("addemployeeinfosignup", cookie),
                           addworker=getword("addworker", cookie), goback=getword("goback", cookie), chatnav=getword("chatnav", cookie))


@addtabs.route("/add/task", methods=["GET", "POST"])
def add_task():

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.accounttype == "worker":
        return redirect(url_for(homepage))

    if current_user.accounttype == "boss":
        workers = Worker.query.filter_by(boss_id=current_user.id).all()
        if workers is None or len(workers) == 0 or workers == [] or workers == "":
            flash(getword("noworkers", cookie), category="error")
            return redirect(url_for(homepage))

    if request.method == 'POST':
        if request.form.get("typeform") == "task":
            date = request.form.get('date')

            if date is None or date == "" or date == " ":
                print("Date is none")
                flash(getword("missingdate", cookie), category="error")
            else:

                datedue = parser.parse(date)

                if datedue < datetime.datetime.now():
                    flash(getword("dateinpast", cookie), category="error")
                    return redirect(url_for('addtabs.add_task'))

                task = request.form.get('task')
                title = request.form.get('title')
                if task == "" or task is None or title == "" or title is None:
                    flash(getword("missingtask", cookie), category="error")
                else:
                    try:
                        workerslist = request.form.getlist('worker')
                        if len(workerslist) == 0:
                            flash(getword("noworkersselected", cookie), category="error")
                            return redirect(url_for(workerspage))
                        workersl = Worker.query.filter(Worker.id.in_(workerslist)).all()
                        tasknum = 0
                        acid = str(uuid.uuid4())
                        for workerg in workersl:
                            tasknum += 1
                            new_task = Task(task=task, title=title, worker_id=workerg.id, boss_id=current_user.id,
                                            actual_id=acid, ordernumber=tasknum, datedue=datedue)
                            db.session.add(new_task)
                            db.session.commit()
                        flash(getword("taskadded", cookie), category="success")
                        redirect(url_for(workerspage))
                    except Exception as e:
                        flash(str(e), category="error")

    return render_template("add_task.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user, idtext=getword("idtext", cookie),
                           addworker=getword("addworker", cookie), delete=getword("delete", cookie),
                           workertext=getword("workertext", cookie), addtask=getword("addtask", cookie),
                           email=getword("email", cookie), name=getword("name", cookie),
                           selectall=getword("selectall", cookie), deselectall=getword("deselectall", cookie),
                           workermenu=getword("workermenu", cookie), submit=getword("submit", cookie),
                           selectworkers=getword("selectworkers", cookie), signupemploy=getword("signupemploy", cookie),
                           here=getword("here", cookie), myfiles=getword("empmyfiles", cookie),
                           addtasktext=getword("addtask", cookie), goback=getword("goback", cookie),
                           tasktext1=getword("tasktext", cookie), titletext1=getword("titletext", cookie), chatnav=getword("chatnav", cookie))
