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

from .translator import getword

views = Blueprint('views', __name__)

homepage = "views.home"
workerspage = "views.workers"
oneworkerpage = "views.worker"

global csrfg


class StatusDenied(Exception):
    print("StatusDenied Exception")


def getcookie(request):
    if 'locale' in request.cookies:
        return request.cookies.get('locale')
    else:
        return 'en'


@views.route('/', methods=['GET'])
def home():

    cookie = getcookie(request)
    return render_template("home.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie),
                           signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie),
                           workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie),
                           logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie),
                           user=current_user, tooltext1=getword("tooltext1", cookie),
                           tooltext2=getword("tooltext2", cookie), tooltext3=getword("tooltext3", cookie),
                           employees=getword("workersnav", cookie), tasks=getword("tasksnav", cookie),
                           register=getword("signup", cookie), login=getword("login", cookie),
                           boss=getword("boss", cookie), worker=getword("worker", cookie),
                           enterpassword=getword("enterpassword", cookie), enteremail=getword("enteremail", cookie),
                           notregistered=getword("notregistered", cookie), registerhere=getword("registerhere", cookie),
                           logout=getword("logout", cookie), profile=getword("profile", cookie),
                           welcome=getword("welcome", cookie), chatnav=getword("chatnav", cookie),
                           newyear=getword("happynewyear", cookie))


@views.route("/home", methods=['GET'])
def homeredirect():
    cookie = getcookie(request)
    return redirect(url_for("views.home"))


def allowed_image(filename):
    allowed_image_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if len(ext) > 3:
        return False

    if ext.lower() in allowed_image_extensions:
        return True
    else:
        return False


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    cookie = getcookie(request)

    return render_template("profile.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user,
                           emailtext=getword("emailshort", request.cookies.get('locale')),
                           nametext=getword("name", request.cookies.get('locale')),
                           profiletext=getword("profiletext", request.cookies.get('locale')),
                           changepassword=getword("changepassword", request.cookies.get('locale')),
                           deleteaccount=getword("deleteaccount", request.cookies.get('locale')),
                           myfiles=getword("myfiles", request.cookies.get('locale')), id=current_user.id,
                           chatnav=getword("chatnav", cookie))


@views.route('/profile/pfp', methods=['GET', 'POST'])
@login_required
def profilepfp():
    cookie = getcookie(request)

    if request.method == 'POST':
        typeform = request.form.get('typeform')
        if typeform == 'pfp':
            for file in request.files.getlist('file'):
                print(file)
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            image = request.files['file']
            if image.filename == '':
                flash(getword("nofileselected", cookie), category="error")
                return redirect(request.url)

            if image.filename == "":
                print("No filename")
                return redirect(views.profilepfp)
            if allowed_image(image.filename):
                from PIL import Image
                filename = secure_filename(image.filename)
                # crop image to square
                image = Image.open(image)
                width, height = image.size
                if width > height:
                    left = (width - height) / 2
                    right = (width + height) / 2
                    top = 0
                    bottom = height
                    image = image.crop((left, top, right, bottom))
                elif height > width:
                    left = 0
                    right = width
                    top = (height - width) / 2
                    bottom = (height + width) / 2
                    image = image.crop((left, top, right, bottom))
                image = image.convert('RGB')
                # check if file exists
                if os.path.isfile(os.path.join(app.config['PFP_UPLOADS'], str(current_user.id) + ".png")):
                    os.remove(os.path.join(app.config['PFP_UPLOADS'], str(current_user.id) + ".png"))
                image.save(os.path.join(app.config["PFP_UPLOADS"], str(current_user.id) + ".png"))
                return redirect(url_for('views.profile'))

    return render_template("profilepfp.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user,
                           emailtext=getword("emailshort", request.cookies.get('locale')),
                           nametext=getword("name", request.cookies.get('locale')),
                           profiletext=getword("profiletext", request.cookies.get('locale')),
                           changepassword=getword("changepassword", request.cookies.get('locale')),
                           deleteaccount=getword("deleteaccount", request.cookies.get('locale')),
                           myfiles=getword("myfiles", request.cookies.get('locale')), id=current_user.id,
                           chatnav=getword("chatnav", cookie), uploadfilebtn=getword("uploadfilebtn", cookie),
                           submit=getword("submit", cookie))


@views.route('/boss')
@login_required
def boss():

    cookie = getcookie(request)

    if current_user.accounttype == "boss":
        return redirect(url_for(homepage))

    if current_user.accounttype == "worker":
        if current_user.boss_id is not None:
            return redirect(url_for(homepage))

    link = "https://tasklify.me/a/" + current_user.registrationid

    return render_template("boss.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie),
                           signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie),
                           workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie),
                           logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie),
                           user=current_user, boss=getword("boss", cookie),
                           accessmessage=getword("accessmessage", cookie), youridtext=getword("youridtext", cookie),
                           id=getword("idemail", cookie), idd=current_user.registrationid, link=link,
                           copy=getword("copy", cookie), chatnav=getword("chatnav", cookie))


@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():

    cookie = getcookie(request)

    if current_user.accounttype == 'worker' and current_user.boss_id is None:
        return redirect(url_for('views.boss'))

    if current_user.accounttype == 'boss':
        return redirect(url_for(workerspage))

    if request.method == 'POST':
        typeform = request.form.get('typeform')
        if typeform == 'done':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task.complete = "2"
            db.session.commit()
        elif typeform == 'notdone':
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            taskpost.complete = "0"
            db.session.commit()
            return redirect(url_for('views.tasks'))

    taskstodisplay = []

    for task in Task.query.filter_by(worker_id=current_user.id).all():
        datedue = task.datedue
        dateformat = time.strftime("%e/%m/%Y - %R", datedue.timetuple())
        taskstodisplay.append(
            {"task": task.task, "complete": task.complete, "actual_id": task.actual_id, "task_id": task.id,
             "title": task.title, "ordernumber": task.ordernumber, "datedue": dateformat, "archive": task.archive})

    taskstodisplay.sort(key=lambda x: x['datedue'], reverse=False)

    for task in taskstodisplay:
        if task['complete'] == "2":
            taskstodisplay.remove(task)
            taskstodisplay.append(task)

    for task in taskstodisplay:
        if task['archive'] == "1":
            taskstodisplay.remove(task)
            taskstodisplay.append(task)

    return render_template("tasks.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie),
                           signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie),
                           workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie),
                           logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie),
                           notdone=getword("notdone", cookie), tasktitle=getword("tasktitle", cookie),
                           moreinfo=getword("moreinfo", cookie), user=current_user, taskslist=taskstodisplay,
                           tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie),
                           workertext=getword("workertext", cookie), done=getword("done", cookie),
                           tasktextplural=getword("tasktextplural", cookie), notstarted=getword("NotStarted", cookie),
                           completed=getword("completed", cookie), started=getword("started", cookie),
                           due=getword("due", cookie), titletext=getword("titletext", cookie),
                           chatnav=getword("chatnav", cookie))


@views.route('/workers/', methods=['GET', 'POST'])
@login_required
def workers():
    allowed_sorts = ['name', 'email', 'tasks']

    cookie = getcookie(request)

    if current_user.is_authenticated:
        if current_user.accounttype == "worker":
            return redirect(url_for(homepage))

    taskstodisplay = []

    if request.method == "POST":
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
                        db.session.commit()
                        flash(getword("workeradded", cookie), category="success")
                    else:
                        flash(getword("workeralreadyadded", cookie), category="error")
        elif request.form.get("typeform") == "delete":
            id = request.form.get('worker_id')
            worker = Worker.query.filter_by(id=id).first()
            if worker.boss_id is not None and worker.boss_id != current_user.id:
                flash(getword("workernotfound", cookie), category="error")

            if worker is None:
                flash(getword("noworkerwithid", cookie), category="error")
            else:
                if worker.boss_id is None:
                    flash(getword("workeralreadyremoved", cookie), category="error")
                else:
                    try:
                        if worker.id.startswith("TEST") or worker.id.startswith("TEST-"):
                            flash("Работника беше премахнат успешно, но тъй като е тестов акаунт, той остава активен!",
                                  category="success")
                            return redirect(url_for('views.workers'))
                        worker.boss_id = None
                        for task in Task.query.filter_by(worker_id=worker.id).all():
                            db.session.delete(task)
                        db.session.commit()
                        flash(getword("workerremoved", cookie), category="success")
                    except Exception as e:
                        flash(e, category="error")
        elif request.form.get("typeform") == "task":
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
                                        actual_id=acid, ordernumber=tasknum)
                        db.session.add(new_task)
                        db.session.commit()
                    flash(getword("taskadded", cookie), category="success")
                    redirect(url_for(workerspage))
                except Exception as e:
                    flash(e, category="error")
        elif request.form.get("typeform") == "workermenu":
            workerid = request.form.get('worker_id')
            return redirect(url_for(oneworkerpage, id=workerid))

    for task in Task.query.filter_by(boss_id=current_user.id).all():
        datedue = task.datedue
        dateformat = time.strftime("%e/%m/%Y - %R", datedue.timetuple())
        taskstodisplay.append(
            {"task": task.task, "complete": task.complete, "actual_id": task.actual_id, "task_id": task.id,
             "title": task.title, "ordernumber": task.ordernumber, "datedue": dateformat, "archive": task.archive})

    taskstodisplay.sort(key=lambda x: x['archive'], reverse=False)

    for task in taskstodisplay:
        if task["ordernumber"] != 1:
            taskstodisplay.remove(task)

    workerslist = []

    for worker in Worker.query.filter_by(boss_id=current_user.id).all():
        workerslist.append({"id": worker.id, "name": worker.first_name, "email": worker.email, "tasks": worker.tasks})

    sort = request.args.get('sort')
    search = request.args.get('search')

    if sort is not None:
        if sort in allowed_sorts:
            if sort == "name":
                workerslist = sorted(workerslist, key=lambda k: k['name'])
            elif sort == "email":
                workerslist = sorted(workerslist, key=lambda k: k['email'])
            elif sort == "tasks":
                undonetasksl = {}
                for worker in workerslist:
                    from . import undonetasks
                    undonetasksl[worker["id"]] = undonetasks(worker["id"])
                workerslist = sorted(workerslist, key=lambda k: undonetasksl[k['id']], reverse=True)

    if search is not None:
        workerslist = [worker for worker in workerslist if
                       search.lower() in worker["name"].lower() or search.lower() in worker["email"].lower()]

    return render_template("workers.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user, idtext=getword("idtext", cookie),
                           addworker=getword("addworker", cookie), delete=getword("delete", cookie),
                           taskslist=taskstodisplay, workertext=getword("workertext", cookie),
                           addtask=getword("addtask", cookie), email=getword("email", cookie),
                           name=getword("name", cookie), selectall=getword("selectall", cookie),
                           deselectall=getword("deselectall", cookie), workermenu=getword("workermenu", cookie),
                           submit=getword("submit", cookie), selectworkers=getword("selectworkers", cookie),
                           signupemploy=getword("signupemploy", cookie), here=getword("here", cookie),
                           myfiles=getword("empmyfiles", cookie), adminpaneltext=getword("adminpaneltext", cookie),
                           addemployeebutton=getword("addemployeebutton", cookie),
                           registeryouremployee=getword("registeryouremployee", cookie),
                           addtasktext=getword("addtasktext", cookie), actiontext=getword("actiontext", cookie),
                           workerslist=workerslist, sorttype=sort, sorttext=getword("sorttext", cookie),
                           sortnametext=getword("sortnametext", cookie), sortemailtext=getword("sortemailtext", cookie),
                           sorttaskstext=getword("sorttaskstext", cookie),
                           currentlysorting=getword("currentlysorting", cookie), nonetext=getword("nonetext", cookie),
                           taskstext=getword("tasksnav", cookie), search=getword("search", cookie),
                           areyousure=getword("areyousure", cookie), chatnav=getword("chatnav", cookie))


@views.route('/worker/<string:id>', methods=["GET", "POST"])
@login_required
def worker(id):

    cookie = getcookie(request)

    if current_user.accounttype == "worker":
        return redirect(url_for(homepage))

    worker = Worker.query.filter_by(id=id).first()
    if worker is None:
        return redirect(url_for(workerspage))
    if worker.boss_id != current_user.id:
        return redirect(url_for(workerspage))

    taskstodisplay = []

    for task in Task.query.filter_by(worker_id=worker.id).all():
        print(task.archive)
        datedue = task.datedue
        dateformat = time.strftime("%e/%m/%Y - %R", datedue.timetuple())
        taskstodisplay.append(
            {"task": task.task, "complete": task.complete, "actual_id": task.actual_id, "task_id": task.id,
             "title": task.title, "ordernumber": task.ordernumber, "datedue": dateformat, "archive": task.archive})

    taskstodisplay.sort(key=lambda x: x['datedue'], reverse=False)
    taskstodisplay.sort(key=lambda x: x['archive'], reverse=False)
    if request.method == "POST":
        typeform = request.form.get('typeform')
        taskid = request.form.get('task_id')

        # check if task exists
        task = Task.query.filter_by(id=taskid).first()
        if task is None:
            flash(getword("tasknotfound", cookie), category="error")
            return redirect(url_for(worker, id=id))

        if Task.query.filter_by(id=taskid).first().boss_id != current_user.id:
            flash(getword("youcantedittask", cookie), category="error")
            return redirect(url_for(workerspage))
        if typeform == 'done':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task.complete = True
            db.session.commit()
            return redirect(url_for(oneworkerpage, id=id))
        elif typeform == 'delete':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task.archive = True
            db.session.commit()
            return redirect(url_for(oneworkerpage, id=id))
        elif typeform == 'notdone':
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            taskpost.complete = False
            db.session.commit()
            return redirect(url_for(oneworkerpage, id=id))
        elif typeform == 'deletefromall':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task_actual_id = task.actual_id
            for task in Task.query.filter_by(actual_id=task_actual_id).all():
                task.archive = True
            db.session.commit()
            return redirect(url_for(oneworkerpage, id=id))
        elif typeform == 'unarchive':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task.archive = False
            db.session.commit()
            return redirect(url_for(oneworkerpage, id=id))
        elif typeform == 'fullydelete':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task_actual_id = task.actual_id
            db.session.delete(task)
            db.session.commit()
            return redirect(url_for(oneworkerpage, id=id))

    return render_template("worker.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), notdone=getword("notdone", cookie),
                           moreinfo=getword("moreinfo", cookie), workerid=id, user=current_user, worker=worker,
                           taskslist=taskstodisplay, tasktext=getword("tasktext", cookie),
                           statustext=getword("statustext", cookie), workertext=getword("workertext", cookie),
                           done=getword("done", cookie), tasktextplural=getword("tasktextplural", cookie),
                           notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie),
                           delete=getword("delete", cookie), started=getword("started", cookie),
                           deletefromall=getword("deletefromall", cookie), workeridtext=getword("workeridtext", cookie),
                           unarchive=getword("unarchive", cookie), fullydelete=getword("fullydelete", cookie),
                           chatnav=getword("chatnav", cookie))


@views.route('/task/<string:id>', methods=["GET", "POST"])
@login_required
def task(id):

    cookie = getcookie(request)

    taskdata = Task.query.filter_by(id=id).first()
    if taskdata is None:
        flash(getword("tasknotfound", cookie), category="error")
        return redirect(url_for(homepage))

    if taskdata.archive:
        flash(getword("tasknotfound", cookie), category="error")
        return redirect(url_for(homepage))

    if current_user.accounttype == "worker":
        if taskdata.worker_id != current_user.id:
            flash(getword("tasknotfound", cookie), category="error")
            return redirect(url_for(homepage))
    elif current_user.accounttype == "boss":
        if taskdata.boss_id != current_user.id:
            flash(getword("tasknotfound", cookie), category="error")
            return redirect(url_for(homepage))

    if request.method == "POST":
        typeform = request.form.get('typeform')
        taskid = request.form.get('task_id')

        if taskid != str(id):
            flash(getword("tasknotfound", cookie), category="error")
            return redirect(url_for("views.task", id=id))

        task = Task.query.filter_by(id=taskid).first()
        if task is None:
            flash(getword("tasknotfound", cookie), category="error")
            return redirect(url_for("views.task", id=id))

        if Task.query.filter_by(id=taskid).first().boss_id != current_user.id:
            if Task.query.filter_by(id=taskid).first().worker_id != current_user.id:
                flash(getword("youcantedittask", cookie), category="error")
                return redirect(url_for("views.task", id=id))

        if typeform == 'done':
            taskid = request.form.get('task_id')
            taskcomment = request.form.get('comment')
            taskpost = Task.query.get(taskid)
            taskpost.complete = "2"
            taskpost.comment = taskcomment
            db.session.commit()
            return redirect(url_for('views.task', id=id))
        elif typeform == 'notdone':
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            taskpost.complete = False
            db.session.commit()
            return redirect(url_for('views.task', id=id))
        elif typeform == "hastebin":
            if request.form.get('commenthaste') == "" or request.form.get('commenthaste') is None:
                flash(getword("nocontent", cookie), category="error")
                return redirect(url_for('views.task', id=id))
            if len(request.form.get('commenthaste')) > 20000:
                flash(getword("toolong20kmax", cookie), category="error")
                return redirect(url_for('views.task', id=id))
            hastebinlink = hastebin(request.form.get('commenthaste'))
            return render_template("task.html", profilenav=getword("profilenav", cookie),
                                   loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                                   tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                                   adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                                   homenav=getword("homenav", cookie),
                                   markyourtaskasdonetext=getword("markyourtaskasdonetext", cookie),
                                   photolinktexttitle=getword("photolinktexttitle", cookie),
                                   photouploader=getword("photouploader", cookie), copy=getword("copy", cookie),
                                   sevendaylimit=getword("sevendaylimit", cookie),
                                   submitcodetext=getword("submitcodetext", cookie), showhastebinmodal=True,
                                   hastebinlink=hastebinlink, print=getword("print", cookie), user=current_user,
                                   notdone=getword("notdone", cookie), task=taskdata.task, task1=taskdata,
                                   title=taskdata.title, taskid=id, done=getword("done", cookie),
                                   tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie),
                                   workertext=getword("workertext", cookie),
                                   tasktextplural=getword("tasktextplural", cookie),
                                   notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie),
                                   delete=getword("delete", cookie), starttext=getword("starttext", cookie),
                                   started=getword("started", cookie), uploadtext=getword("uploadtext", cookie),
                                   datedue=dateformat, due=getword("due", cookie),
                                   fileuploader=getword("fileuploader", cookie), titletext=getword("titletext", cookie),
                                   desctext=getword("desctext", cookie), chatnav=getword("chatnav", cookie))
        elif typeform == "uploadimage":
            ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash(getword("nofileselected", cookie), category="error")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # check file size
                if file.content_length > 15000000:
                    flash(getword("filetoobig15mb", cookie), category="error")
                    return redirect(url_for('views.task', id=id))
                # check if file is suspicious
                suspicious_file_types = ['application/x-dosexec', 'application/x-msdownload',
                                         'application/x-msdos-program', 'application/x-msi', 'application/x-winexe',
                                         'application/x-shockwave-flash', 'application/x-shockwave-flash2-preview',
                                         'application/x-java-applet', 'application/x-java-bean',
                                         'application/x-java-vm', ]
                if file.content_type in suspicious_file_types:
                    flash(getword("wecannotacceptthisfile", cookie), category="error")
                    return redirect(url_for('views.task', id=id))
                filename = secure_filename(file.filename)
                finalfilename = str(current_user.id) + "_" + filename
                UPLOADS_PATH = join(dirname(realpath(__file__)), 'ugc/uploads/')
                path = join(UPLOADS_PATH, finalfilename)
                file.save(path)
                imageurl = url_for('fileshandler.uploaded_file', filename=finalfilename)

                datedue = taskdata.datedue
                dateformat = time.strftime("%e/%m/%Y - %R", datedue.timetuple())

                return render_template("task.html", profilenav=getword("profilenav", cookie),
                                       loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                                       tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                                       adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                                       homenav=getword("homenav", cookie),
                                       markyourtaskasdonetext=getword("markyourtaskasdonetext", cookie),
                                       photolinktexttitle=getword("photolinktexttitle", cookie),
                                       photouploader=getword("photouploader", cookie), showimagemodal=True,
                                       imageurl=imageurl, copy=getword("copy", cookie), hastebinlink=None,
                                       showhastebinmodal=False, sevendaylimit=getword("sevendaylimit", cookie),
                                       submitcodetext=getword("submitcodetext", cookie), print=getword("print", cookie),
                                       user=current_user, notdone=getword("notdone", cookie), task=taskdata.task,
                                       task1=taskdata, title=taskdata.title, taskid=id, done=getword("done", cookie),
                                       tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie),
                                       workertext=getword("workertext", cookie),
                                       tasktextplural=getword("tasktextplural", cookie),
                                       notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie),
                                       delete=getword("delete", cookie), starttext=getword("starttext", cookie),
                                       started=getword("started", cookie), uploadtext=getword("uploadtext", cookie),
                                       datedue=dateformat, due=getword("due", cookie),
                                       fileuploader=getword("fileuploader", cookie),
                                       titletext=getword("titletext", cookie), desctext=getword("desctext", cookie),
                                       chatnav=getword("chatnav", cookie), comment=getword("comment", cookie))
            else:
                flash(getword("invalidtype", cookie), category="error")
                return redirect(url_for('views.task', id=id))
        elif typeform == "start":
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            taskpost.complete = "1"
            db.session.commit()
            return redirect(url_for('views.task', id=id))
        elif typeform == "uploadzip":
            ALLOWED_EXTENSIONS1 = ['zip', 'rar', '7z']

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS1

            if 'file' not in request.files:
                flash('No file part', category="error")
                return redirect(request.url)

            file = request.files['file']
            if file.filename == '':
                flash(getword("nofileselected", cookie), category="error")
                return redirect(url_for('views.task', id=id))
            if file and allowed_file(file.filename):
                # check file size
                if file.content_length > 200000000:
                    flash("File too big! 200MB", category="error")
                    return redirect(url_for('views.task', id=id))
                # check if file is suspicious
                suspicious_file_types = ['application/x-dosexec', 'application/x-msdownload',
                                         'application/x-msdos-program', 'application/x-msi', 'application/x-winexe',
                                         'application/x-shockwave-flash', 'application/x-shockwave-flash2-preview',
                                         'application/x-java-applet', 'application/x-java-bean',
                                         'application/x-java-vm', ]
                if file.content_type in suspicious_file_types:
                    flash(getword("wecannotacceptthisfile", cookie), category="error")
                    return redirect(url_for('views.task', id=id))
                filename = secure_filename(file.filename)
                finalfilename = str(current_user.id) + "_" + filename
                UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
                path = join(UPLOADS_PATH, finalfilename)
                file.save(path)
                imageurl = url_for('fileshandler.uploaded_file', filename=finalfilename)
                datedue = taskdata.datedue
                dateformat = time.strftime("%e/%m/%Y - %R", datedue.timetuple())
                return render_template("task.html", profilenav=getword("profilenav", cookie),
                                       loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                                       tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                                       adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                                       homenav=getword("homenav", cookie),
                                       markyourtaskasdonetext=getword("markyourtaskasdonetext", cookie),
                                       photolinktexttitle=getword("photolinktexttitle", cookie),
                                       photouploader=getword("photouploader", cookie), showimagemodal=True,
                                       imageurl=imageurl, copy=getword("copy", cookie), hastebinlink=None,
                                       showhastebinmodal=False, sevendaylimit=getword("sevendaylimit", cookie),
                                       submitcodetext=getword("submitcodetext", cookie), print=getword("print", cookie),
                                       user=current_user, notdone=getword("notdone", cookie), task=taskdata.task,
                                       task1=taskdata, title=taskdata.title, taskid=id, done=getword("done", cookie),
                                       tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie),
                                       workertext=getword("workertext", cookie),
                                       tasktextplural=getword("tasktextplural", cookie),
                                       notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie),
                                       delete=getword("delete", cookie), starttext=getword("starttext", cookie),
                                       started=getword("started", cookie), uploadtext=getword("uploadtext", cookie),
                                       datedue=dateformat, due=getword("due", cookie),
                                       fileuploader=getword("fileuploader", cookie),
                                       titletext=getword("titletext", cookie), desctext=getword("desctext", cookie),
                                       chatnav=getword("chatnav", cookie), comment=getword("comment", cookie))

            else:
                flash(getword("invalidtype", cookie), category="error")
                return redirect(url_for('views.task', id=id))

    datedue = taskdata.datedue
    dateformat = time.strftime("%e/%m/%Y - %R", datedue.timetuple())

    return render_template("task.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie),
                           signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie),
                           workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie),
                           logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie),
                           markyourtaskasdonetext=getword("markyourtaskasdonetext", cookie),
                           photolinktexttitle=getword("photolinktexttitle", cookie),
                           photouploader=getword("photouploader", cookie), copy=getword("copy", cookie),
                           sevendaylimit=getword("sevendaylimit", cookie),
                           submitcodetext=getword("submitcodetext", cookie), showimagemodal=False,
                           showhastebinmodal=False, hastebinlink=None, print=getword("print", cookie),
                           user=current_user, notdone=getword("notdone", cookie), task=taskdata.task, task1=taskdata,
                           title=taskdata.title, taskid=id, done=getword("done", cookie),
                           tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie),
                           workertext=getword("workertext", cookie), tasktextplural=getword("tasktextplural", cookie),
                           notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie),
                           delete=getword("delete", cookie), starttext=getword("starttext", cookie),
                           started=getword("started", cookie), uploadtext=getword("uploadtext", cookie),
                           datedue=dateformat, due=getword("due", cookie), fileuploader=getword("fileuploader", cookie),
                           titletext=getword("titletext", cookie), desctext=getword("desctext", cookie),
                           chatnav=getword("chatnav", cookie), comment=getword("comment", cookie))


@views.route('/urlout/<path:url>', methods=["GET", "POST"])
def urlout(url):
    abort(403)
    cookie = getcookie(request)
    return render_template("urlout.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), url=url, user=current_user,
                           youllberedirectedto=getword("youllberedirectedto", cookie), here=getword("here", cookie),
                           ifyourenotredirected=getword("ifyourenotredirected", cookie),
                           oryoucango=getword("oryoucango", cookie), home=getword("home", cookie),
                           thirdpartylink=getword("thirdpartylink", cookie),
                           infiveseconds=getword("infiveseconds", cookie), chatnav=getword("chatnav", cookie))


@views.route('/contact', methods=["GET", "POST"])
def contact():
    from .mailsender import sendmail

    cookie = getcookie(request)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        if len(name) < 1:
            flash(getword("invalidname", cookie), category="error")
        elif len(email) < 4:
            flash(getword("invalidemail", cookie), category="error")
        elif len(message) < 1:
            flash(getword("invalidmessage", cookie), category="error")
        else:
            sendmail(name, email, message)
            flash(getword("emailsent", cookie), category="success")
            return redirect(url_for('views.contact'))

    return render_template("contact.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user,
                           contactus=getword("contactus", cookie), contactusmessage=getword("contactusmessage", cookie),
                           contactname=getword("contactname", cookie), contactemail=getword("contactemail", cookie),
                           contactname2=getword("contactname2", cookie), contactemail2=getword("contactemail2", cookie),
                           name=getword("name", cookie), email=getword("email", cookie),
                           message=getword("message", cookie), chatnav=getword("chatnav", cookie))


@views.route('/testpastebin', methods=["GET", "POST"])
def testpastebin():
    abort(403)
    return "false"


@views.route("/printtask/<int:id>", methods=["GET", "POST"])
def printtask(id):
    abort(403)

    # cookie
    cookie = getcookie(request)

    taskdata = Task.query.filter_by(id=id).first()

    worker = Worker.query.filter_by(id=taskdata.worker_id).first()
    worker_id = worker.id
    workername = worker.first_name
    workeremail = worker.email

    if taskdata is None:
        flash(getword("tasknotfound", cookie), category="error")
        return redirect(url_for(homepage))

    if current_user.accounttype == "worker":
        if taskdata.worker_id != current_user.id:
            flash(getword("tasknotfound", cookie), category="error")
            return redirect(url_for(homepage))

    elif current_user.accounttype == "boss":
        if taskdata.boss_id != current_user.id:
            flash(getword("tasknotfound", cookie), category="error")
            return redirect(url_for(homepage))

    return render_template("printtask.html", profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user, task=taskdata.task, task1=taskdata,
                           title=taskdata.title, taskid=id, workerid=worker_id, notdone=getword("notdone", cookie),
                           workeremail=workeremail, workername=workername, boss=current_user.first_name, cookie=cookie,
                           workeridtext=getword("workeridtext", cookie),
                           workeremailtext=getword("workeremailtext", cookie),
                           workernametext=getword("workernametext", cookie),
                           taskstatustext=getword("taskstatustext", cookie), attext=getword("attext", cookie),
                           requestedbytext=getword("requestedbytext", cookie),
                           startedtext=getword("startedtext", cookie), chatnav=getword("chatnav", cookie))


@views.route("/docs", methods=["GET"], subdomain="docs")
def docs():
    return "Under construction"


@views.route("/cookies-disabled", methods=["GET"])
def cookies_disabled():
    return render_template("cookies_disabled.html", user=current_user)


@views.route("/offline", methods=["GET"])
def offline():
    abort(403)


@views.route("/privacy", methods=["GET"])
def privacy():
    cookie = getcookie(request)

    return render_template("privacy.html", user=current_user, privacypolicytitle=getword("privacypolicytitle", cookie),
                           privacypolicytext1=getword("privacypolicytext1", cookie),
                           privacypolicytext2=getword("privacypolicytext2", cookie),
                           privacypolicytext3=getword("privacypolicytext3", cookie),
                           privacypolicytext4=getword("privacypolicytext4", cookie),
                           privacypolicytext5=getword("privacypolicytext5", cookie),
                           privacypolicytext6=getword("privacypolicytext6", cookie),
                           privacypolicytext7=getword("privacypolicytext7", cookie),
                           privacypolicytext8=getword("privacypolicytext8", cookie),
                           privacypolicytext9=getword("privacypolicytext9", cookie),
                           privacypolicytext10=getword("privacypolicytext10", cookie),
                           privacypolicytext11=getword("privacypolicytext11", cookie),
                           privacypolicytext12=getword("privacypolicytext12", cookie),
                           privacypolicytext13=getword("privacypolicytext13", cookie),
                           chatnav=getword("chatnav", cookie))
