import json

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from flask_login import login_required, current_user

from . import db
from .models import Worker, Boss, Task
from .translator import getword, loadtime
import uuid
import urllib
import urllib.parse
import urllib.request
import urllib.error
import requests


views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    abort(403)
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    abort(403)
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user, emailtext=getword("emailshort", request.cookies.get('locale')), nametext=getword("name", request.cookies.get('locale')), profiletext=getword("profiletext", request.cookies.get('locale')), changepassword=getword("changepassword", request.cookies.get('locale')), deleteaccount=getword("deleteaccount", request.cookies.get('locale')))


@views.route('/boss')
@login_required
def boss():
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.accounttype == "boss":
        return redirect(url_for('views.home'))

    if current_user.accounttype == "worker":
        if current_user.boss_id is not None:
            return redirect(url_for('views.home'))

    return render_template("boss.html", user=current_user, boss=getword("boss", cookie), accessmessage=getword("accessmessage", cookie), youridtext=getword("youridtext", cookie), id=current_user.registrationid)


@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.accounttype == 'worker' and current_user.boss_id is None:
        return redirect(url_for('views.boss'))

    if current_user.accounttype == 'boss':
        return redirect(url_for('views.workers'))

    if request.method == 'POST':
        typeform = request.form.get('typeform')
        if typeform == 'done':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task.complete = True
            db.session.commit()
        elif typeform == 'notdone':
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            taskpost.complete = False
            db.session.commit()
            return redirect(url_for('views.tasks'))

    taskstodisplay = []

    for task in Task.query.filter_by(worker_id=current_user.id).all():
        taskstodisplay.append({"task": task.task, "complete": task.complete, "actual_id": task.actual_id,
                               "task_id": task.id, "title": task.title, "ordernumber": task.ordernumber})

    return render_template("tasks.html", notdone=getword("notdone", cookie), tasktitle=getword("tasktitle", cookie), moreinfo=getword("moreinfo", cookie), user=current_user, taskslist=taskstodisplay, tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie), workertext=getword("workertext", cookie), done=getword("done", cookie), tasktextplural=getword("tasktextplural", cookie), notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie))


@views.route('/workers', methods=["GET", "POST"])
@login_required
def workers():
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.is_authenticated:
        if current_user.accounttype == "worker":
            return redirect(url_for('views.home'))

    taskstodisplay = []

    if request.method == "POST":
        if request.form.get("typeform") == "add":
            print("adding worker")
            id = request.form.get('ID')

            if id == "" or id is None:
                flash("Missing ID", category="error")
            else:
                worker = Worker.query.filter_by(registrationid=id).first()
                if worker is None:
                    flash("No worker with that ID", category="error")
                else:
                    if worker.boss_id is None:
                        worker.boss_id = current_user.id
                        db.session.commit()
                        flash("Worker added", category="success")
                    else:
                        flash("Worker already added", category="error")
        elif request.form.get("typeform") == "delete":
            id = request.form.get('worker_id')
            worker = Worker.query.filter_by(registrationid=id).first()
            if worker is None:
                flash("No worker with that ID", category="error")
            else:
                if worker.boss_id is None:
                    flash("Worker already removed", category="error")
                else:
                    try:
                        worker.boss_id = None
                        for task in Task.query.filter_by(worker_id=worker.id).all():
                            db.session.delete(task)
                        db.session.commit()
                        flash("Worker removed", category="success")
                    except Exception as e:
                        flash(e, category="error")
        elif request.form.get("typeform") == "task":
            task = request.form.get('task')
            title = request.form.get('title')
            if task == "" or task is None or title == "" or title is None:
                flash("Missing task", category="error")
            else:
                try:
                    workerslist = request.form.getlist('worker')
                    if len(workerslist) == 0:
                        flash("No workers selected", category="error")
                        return redirect(url_for('views.workers'))
                    workersl = Worker.query.filter(Worker.id.in_(workerslist)).all()
                    tasknum = 0
                    acid = str(uuid.uuid4())
                    for workerg in workersl:
                        tasknum += 1
                        print(tasknum)
                        new_task = Task(task=task, title=title, worker_id=workerg.id, boss_id=current_user.id, actual_id=acid, ordernumber=tasknum)
                        print(new_task)
                        db.session.add(new_task)
                        db.session.commit()
                    flash("Task added", category="success")
                    redirect(url_for('views.workers'))
                except Exception as e:
                    flash(e, category="error")
        elif request.form.get("typeform") == "workermenu":
            workerid = request.form.get('worker_id')
            return redirect(url_for('views.worker', id=workerid))

    for task in Task.query.filter_by(boss_id=current_user.id).all():
        taskstodisplay.append({"task": task.task, "actual_id": task.actual_id, "ordernumber": task.ordernumber})
    for task in taskstodisplay:
        if task["ordernumber"] != 1:
            taskstodisplay.remove(task)

    return render_template("workers.html", user=current_user, idtext=getword("idtext", cookie), addworker=getword("addworker", cookie), delete=getword("delete", cookie), taskslist=taskstodisplay, workertext=getword("workertext", cookie), addtask=getword("addtask", cookie), email=getword("email", cookie), name=getword("name", cookie), selectall=getword("selectall", cookie), deselectall=getword("deselectall", cookie), workermenu=getword("workermenu", cookie), submit=getword("submit", cookie), selectworkers=getword("selectworkers", cookie))


@views.route('/worker/<path:id>', methods=["GET", "POST"])
@login_required
def worker(id):
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.accounttype == "worker":
        return redirect(url_for('views.home'))

    worker = Worker.query.filter_by(id=id).first()
    if worker is None:
        return redirect(url_for('views.workers'))
    if worker.boss_id != current_user.id:
        return redirect(url_for('views.workers'))

    taskstodisplay = []

    for task in Task.query.filter_by(worker_id=worker.id).all():
        taskstodisplay.append({"task": task.task, "complete": task.complete, "actual_id": task.actual_id,
                               "task_id": task.id, "ordernumber": task.ordernumber, "title": task.title,
                               "comment": task.comment})
    if request.method == "POST":
        typeform = request.form.get('typeform')
        if typeform == 'done':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task.complete = True
            db.session.commit()
            return redirect(url_for('views.worker', id=id))
        elif typeform == 'delete':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            db.session.delete(task)
            db.session.commit()
            return redirect(url_for('views.worker', id=id))
        elif typeform == 'notdone':
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            taskpost.complete = False
            db.session.commit()
            return redirect(url_for('views.worker', id=id))

    return render_template("worker.html", notdone=getword("notdone", cookie), moreinfo=getword("moreinfo", cookie), workerid=id, user=current_user, worker=worker, taskslist=taskstodisplay, tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie), workertext=getword("workertext", cookie), done=getword("done", cookie), tasktextplural=getword("tasktextplural", cookie), notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie), delete=getword("delete", cookie))


@views.route('/task/<int:id>', methods=["GET", "POST"])
@login_required
def task(id):
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    taskdata = Task.query.filter_by(id=id).first()
    if taskdata is None:
        flash("Task not found", category="error")
        return redirect(url_for('views.home'))

    if current_user.accounttype == "worker":
        if taskdata.worker_id != current_user.id:
            flash("Task not found", category="error")
            return redirect(url_for('views.home'))
    elif current_user.accounttype == "boss":
        if taskdata.boss_id != current_user.id:
            flash("Task not found", category="error")
            return redirect(url_for('views.home'))

    if request.method == "POST":
        typeform = request.form.get('typeform')
        if typeform == 'done':
            taskid = request.form.get('task_id')
            taskcomment = request.form.get('comment')
            taskpost = Task.query.get(taskid)
            taskpost.complete = True
            taskpost.comment = taskcomment
            db.session.commit()
            return redirect(url_for('views.task', id=id))
        elif typeform == 'notdone':
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            taskpost.complete = False
            db.session.commit()
            return redirect(url_for('views.task', id=id))

    return render_template("task.html", user=current_user, notdone=getword("notdone", cookie), task=taskdata.task, task1=taskdata, title=taskdata.title, taskid=id, done=getword("done", cookie), tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie), workertext=getword("workertext", cookie), tasktextplural=getword("tasktextplural", cookie), notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie), delete=getword("delete", cookie))


@views.route('/urlout/<path:url>', methods=["GET", "POST"])
def urlout(url):
    abort(403)
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'
    return render_template("urlout.html", url=url, user=current_user, youllberedirectedto=getword("youllberedirectedto", cookie), here=getword("here", cookie), ifyourenotredirected=getword("ifyourenotredirected", cookie), oryoucango=getword("oryoucango", cookie), home=getword("home", cookie), thirdpartylink=getword("thirdpartylink", cookie), infiveseconds=getword("infiveseconds", cookie))


@views.route('/contact', methods=["GET", "POST"])
def contact():
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    return render_template("contact.html", user=current_user,
                           contactus=getword("contactus", cookie),
                           contactusmessage=getword("contactusmessage", cookie),
                           contactname=getword("contactname", cookie),
                           contactemail=getword("contactemail", cookie))



@views.route('/testpastebin', methods=["GET", "POST"])
def testpastebin():
    abort(403)
    return "false"

