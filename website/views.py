import json
import os
import uuid
from os.path import join, dirname, realpath

import requests
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from flask import current_app as app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename, send_from_directory

from . import db
from .models import Worker, Boss, Task
from .translator import getword

views = Blueprint('views', __name__)




global csrfg


class StatusDenied(Exception):
    print("StatusDenied Exception")


@views.errorhandler(StatusDenied)
def redirect_on_status_denied(error):
    print(error)
    return render_template("maintenance.html"), 403

def checkmaintenance():
    pass
    # try:
    #     r = requests.get("https://api.npoint.io/fdd18b346a9f50481a65")
    #     if r.json()["status"] == "maintain":
    #         print("maintenance 1")
    #         raise StatusDenied()
    #     else:
    #         pass
    # except:
    #     raise StatusDenied()

@views.route('/', methods=['GET'])
def home():
    checkmaintenance()
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
    checkmaintenance()
    return render_template("profile.html", user=current_user, emailtext=getword("emailshort", request.cookies.get('locale')), nametext=getword("name", request.cookies.get('locale')), profiletext=getword("profiletext", request.cookies.get('locale')), changepassword=getword("changepassword", request.cookies.get('locale')), deleteaccount=getword("deleteaccount", request.cookies.get('locale')))


@views.route('/boss')
@login_required
def boss():
    checkmaintenance()
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
    checkmaintenance()
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
    checkmaintenance()
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
    checkmaintenance()
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

@views.route('uploaded_file/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    checkmaintenance()

    if not current_user.is_authenticated:
        flash("You need to be logged in to view this page", category="error")
        return redirect(url_for('auth.login'))

    print(filename)
    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        if current_user.accounttype == "worker":
            print("worker")
            imageid = filename.split("_")[0]

            # check if imageid is either workerid or bossid
            worker = Worker.query.filter_by(id=imageid).first()
            if worker is None:
                boss = Boss.query.filter_by(id=imageid).first()
                if boss is None:
                    return redirect(url_for('views.home'))
                else:
                    if current_user.boss_id != boss.id:
                        return redirect(url_for('views.home'))
            else:
                if worker.id != current_user.id:
                    return redirect(url_for('views.home'))
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)


        elif current_user.accounttype == "boss":
            print("boss")
            imageid = filename.split("_")[0]
            print(imageid)
            if Boss.query.filter_by(id=imageid).first() is not None:
                if Boss.query.filter_by(id=imageid).first().id == current_user.id:
                    print(Boss.query.filter_by(id=imageid).first().id)
                    print(current_user.id)
                    print("yes")
                    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)
            elif Worker.query.filter_by(id=imageid).first() is not None:
                if Worker.query.filter_by(id=imageid).first().boss_id == current_user.id:
                    print("yes")
                    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)

            flash("You don't have permission to view this file", category="error")
            return redirect(url_for('views.home'))

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)

@views.route("/static/uploads/<path:filename>", methods=["GET"])
def get_file(filename):
    return redirect(url_for('views.uploaded_file', filename=filename))





def hastebin(text):
    r = requests.post("https://hastebin.com/documents", data=text)
    return "https://hastebin.com/raw/" + r.json()["key"]


# def uploadimage(image):
#     r = requests.post(f"https://freeimage.host/api/1/upload?key=6d207e02198a847aa98d0a2a901485a5&source={image_string}&format=json")
#
#     return r.json()


@views.route('/task/<int:id>', methods=["GET", "POST"])
@login_required
def task(id):
    checkmaintenance()
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
        elif typeform == "hastebin":
            if request.form.get('commenthaste') == "" or request.form.get('commenthaste') is None:
                flash("No conent", category="error")
                return redirect(url_for('views.task', id=id))
            if len(request.form.get('commenthaste')) > 20000:
                flash("Too long! 20000 character max", category="error")
                return redirect(url_for('views.task', id=id))
            hastebinlink = hastebin(request.form.get('commenthaste'))
            return render_template("task.html", markyourtaskasdonetext=getword("markyourtaskasdonetext", cookie), photolinktexttitle=getword("photolinktexttitle", cookie), photouploader=getword("photouploader", cookie), copy=getword("copy", cookie), sevendaylimit=getword("sevendaylimit", cookie), submitcodetext=getword("submitcodetext", cookie), showhastebinmodal=True, hastebinlink=hastebinlink, print=getword("print", cookie), user=current_user, notdone=getword("notdone", cookie), task=taskdata.task, task1=taskdata, title=taskdata.title, taskid=id, done=getword("done", cookie), tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie), workertext=getword("workertext", cookie), tasktextplural=getword("tasktextplural", cookie), notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie), delete=getword("delete", cookie))
        elif typeform == "uploadimage":
            ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

            print(request.files)
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # check file size
                if file.content_length > 15000000:
                    flash("Max file size is 15MB", category="error")
                    return redirect(url_for('views.task', id=id))
                # check if file is suspicious
                suspicious_file_types = [
                    'application/x-dosexec',
                    'application/x-msdownload',
                    'application/x-msdos-program',
                    'application/x-msi',
                    'application/x-winexe',
                    'application/x-shockwave-flash',
                    'application/x-shockwave-flash2-preview',
                    'application/x-java-applet',
                    'application/x-java-bean',
                    'application/x-java-vm',
                ]
                if file.content_type in suspicious_file_types:
                    flash("We cannot accept this file type", category="error")
                    return redirect(url_for('views.task', id=id))
                print("uploading")
                filename = secure_filename(file.filename)
                finalfilename = str(current_user.id) + "_" + filename
                UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
                path = join(UPLOADS_PATH, finalfilename)
                file.save(path)
                imageurl = url_for('views.uploaded_file', filename=finalfilename)
                print(imageurl)

                return render_template("task.html", markyourtaskasdonetext=getword("markyourtaskasdonetext", cookie), photolinktexttitle=getword("photolinktexttitle", cookie), photouploader=getword("photouploader", cookie), showimagemodal=True, imageurl=imageurl, copy=getword("copy", cookie), hastebinlink=None, showhastebinmodal=False, sevendaylimit=getword("sevendaylimit", cookie), submitcodetext=getword("submitcodetext", cookie), print=getword("print", cookie), user=current_user, notdone=getword("notdone", cookie), task=taskdata.task, task1=taskdata, title=taskdata.title, taskid=id, done=getword("done", cookie), tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie), workertext=getword("workertext", cookie), tasktextplural=getword("tasktextplural", cookie), notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie), delete=getword("delete", cookie))
            else:
                flash("Invalid Format. Allowed file types are txt, pdf, png, jpg, jpeg, gif", category="error")
                return redirect(url_for('views.task', id=id))



    return render_template("task.html", markyourtaskasdonetext=getword("markyourtaskasdonetext", cookie), photolinktexttitle=getword("photolinktexttitle", cookie), photouploader=getword("photouploader", cookie), copy=getword("copy", cookie), sevendaylimit=getword("sevendaylimit", cookie), submitcodetext=getword("submitcodetext", cookie), showimagemodal=False, showhastebinmodal=False, hastebinlink=None, print=getword("print", cookie), user=current_user, notdone=getword("notdone", cookie), task=taskdata.task, task1=taskdata, title=taskdata.title, taskid=id, done=getword("done", cookie), tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie), workertext=getword("workertext", cookie), tasktextplural=getword("tasktextplural", cookie), notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie), delete=getword("delete", cookie))


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
    checkmaintenance()
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    return render_template("contact.html", user=current_user, contactus=getword("contactus", cookie), contactusmessage=getword("contactusmessage", cookie), contactname=getword("contactname", cookie), contactemail=getword("contactemail", cookie))


@views.route('/testpastebin', methods=["GET", "POST"])
def testpastebin():
    abort(403)
    return "false"


@views.route("/printtask/<int:id>", methods=["GET", "POST"])
def printtask(id):
    checkmaintenance()
    # cookie
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    taskdata = Task.query.filter_by(id=id).first()

    worker = Worker.query.filter_by(id=taskdata.worker_id).first()
    worker_id = worker.id
    workername = worker.first_name
    workeremail = worker.email

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

    return render_template("printtask.html", user=current_user, task=taskdata.task, task1=taskdata, title=taskdata.title, taskid=id, workerid=worker_id, notdone=getword("notdone", cookie), workeremail=workeremail, workername=workername, boss=current_user.first_name, cookie=cookie, workeridtext=getword("workeridtext", cookie), workeremailtext=getword("workeremailtext", cookie), workernametext=getword("workernametext", cookie), taskstatustext=getword("taskstatustext", cookie), attext=getword("attext", cookie), requestedbytext=getword("requestedbytext", cookie))

@views.route("/files/<path:id>", methods=["GET", "POST"])
def files(id):

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.accounttype == "worker":
        if current_user.id != id:
            flash("Not found", category="error")
            return redirect(url_for('views.home'))
    elif current_user.accounttype == "boss":
        if current_user.id != id:
            flash("Not found", category="error")
            return redirect(url_for('views.home'))
        elif Boss.query.filter_by(id=id).first().id != current_user.id:
            flash("Not found", category="error")
            return redirect(url_for('views.home'))

    # check static/uploads for files starting with id
    files = []
    splitnames = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        # split by _
        file1 = file.split("_")
        if str(file1[0]) == str(id):
            files.append(file)




    print(files)
    return render_template("files.html", user=current_user, files=files, splitnames=splitnames)
