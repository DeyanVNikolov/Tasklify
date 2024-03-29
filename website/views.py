import datetime
import os
import random
import time
import uuid
from random import randint

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask import current_app as app
from flask_login import login_required, current_user
from transliterate import translit
from werkzeug.utils import secure_filename

from . import db
from .models import Task
from .models import Worker, Boss
from .translator import getword, gettheme, sharefile

views = Blueprint('views', __name__)

homepage = "views.home"
workerspage = "views.workers"
oneworkerpage = "views.worker"

global csrfg


def getcookie(request):
    if 'locale' in request.cookies:
        return request.cookies.get('locale')
    else:
        return 'en'


@views.route('/banned', methods=['GET'])
def banned():
    return render_template("banned.html", cookie=getcookie(request))


@views.route('/', methods=['GET'])
def home():
    cookie = getcookie(request)
    return render_template("home.html",calendar=getword("calendar", cookie), cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user,
                           tooltext1=getword("tooltext1", cookie), tooltext2=getword("tooltext2", cookie),
                           tooltext3=getword("tooltext3", cookie), employees=getword("workersnav", cookie),
                           tasks=getword("tasksnav", cookie), register=getword("signup", cookie),
                           login=getword("login", cookie), boss=getword("boss", cookie),
                           worker=getword("worker", cookie), enterpassword=getword("enterpassword", cookie),
                           enteremail=getword("enteremail", cookie), notregistered=getword("notregistered", cookie),
                           registerhere=getword("registerhere", cookie), logout=getword("logout", cookie),
                           profile=getword("profile", cookie), welcome=getword("welcome", cookie),
                           chatnav=getword("chatnav", cookie), newyear=getword("happynewyear", cookie),
                           employee=getword("employee", cookie), youareloggedinas=getword("youareloggedinas", cookie),
                           idtext=getword("idtext", cookie), welcometotasklify=getword("welcometotasklify", cookie),
                           getstartednow=getword("getstartednow", cookie),
                           maketaskalloc=getword("maketaskalloc", cookie), cookiet=cookie, theme=gettheme(request))


@views.route("/home", methods=['GET'])
def homeredirect():
    return redirect(url_for("views.home"))


def allowed_image(filename):
    allowed_image_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if "." not in filename:
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

    return render_template("profile.html",calendar=getword("calendar", cookie), cookie=getcookie(request), profilenav=getword("profilenav", cookie),
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
                           chatnav=getword("chatnav", cookie), idtext=getword("idtext", cookie),
                           changeprofilepicture=getword("changeprofilepicture", cookie), theme=gettheme(request))


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

    return render_template("profilepfp.html",calendar=getword("calendar", cookie), cookie=getcookie(request), profilenav=getword("profilenav", cookie),
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
                           submit=getword("submit", cookie), theme=gettheme(request))


@views.route('/profile/set2fa', methods=['GET', 'POST'])
@login_required
def profileset2fa():

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    return render_template("profileset2fa.html",calendar=getword("calendar", cookie), cookie=getcookie(request), profilenav=getword("profilenav", cookie),
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
                           submit=getword("submit", cookie), theme=gettheme(request), factor=current_user.factor)


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

    return render_template("boss.html",calendar=getword("calendar", cookie), cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user, boss=getword("boss", cookie),
                           accessmessage=getword("accessmessage", cookie), youridtext=getword("youridtext", cookie),
                           id=getword("idemail", cookie), idd=current_user.registrationid, link=link,
                           copy=getword("copy", cookie), chatnav=getword("chatnav", cookie), theme=gettheme(request))


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
            if current_user.id != task.worker_id:
                if current_user.id != task.boss_id:
                    return redirect(url_for('views.tasks'))
            task.complete = "2"
            db.session.commit()
        elif typeform == 'started':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            if current_user.id != task.worker_id:
                if current_user.id != task.boss_id:
                    return redirect(url_for('views.tasks'))
            task.complete = "1"
            db.session.commit()
        elif typeform == 'notdone':
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            if current_user.id != taskpost.worker_id:
                if current_user.id != taskpost.boss_id:
                    return redirect(url_for('views.tasks'))
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

    taskstodisplay.sort(key=lambda x: x['datedue'], reverse=True)

    return render_template("tasks.html",calendar=getword("calendar", cookie), cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), notdone=getword("notdone", cookie),
                           tasktitle=getword("tasktitle", cookie), moreinfo=getword("moreinfo", cookie),
                           user=current_user, taskslist=taskstodisplay, tasktext=getword("tasktext", cookie),
                           statustext=getword("statustext", cookie), workertext=getword("workertext", cookie),
                           done=getword("done", cookie), tasktextplural=getword("tasktextplural", cookie),
                           notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie),
                           started=getword("started", cookie), due=getword("due", cookie),
                           titletext=getword("titletext", cookie), chatnav=getword("chatnav", cookie),
                           currentlysorting=getword("currentlysorting", cookie), theme=gettheme(request))


@views.route('/workers/', methods=['GET', 'POST'])
@login_required
def workers():
    allowed_sorts = ['name', 'email', 'tasks']

    cookie = getcookie(request)

    if current_user.is_authenticated:
        if current_user.accounttype == "worker":
            return redirect(url_for(homepage))

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
        elif request.form.get("typeform") == 'deletetask':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            db.session.delete(task)
            db.session.commit()
            return redirect(url_for(workerspage))
        elif request.form.get("typeform") == 'started':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task.complete = "1"
            db.session.commit()
            return redirect(url_for(workerspage))
        elif request.form.get("typeform") == 'notdone':
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            taskpost.complete = "0"
            db.session.commit()
            return redirect(url_for(workerspage))
        elif request.form.get("typeform") == 'done':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task.complete = "2"
            db.session.commit()
            return redirect(url_for(workerspage))

    taskstodisplay = []

    for task in Task.query.filter_by(boss_id=current_user.id).all():
        datedue = task.datedue
        dateformat = time.strftime("%e/%m/%Y - %R", datedue.timetuple())
        task_worker = Worker.query.filter_by(id=task.worker_id).first()
        date_due_in_unix = int(time.mktime(datedue.timetuple()))
        taskstodisplay.append(
            {"task": task.task, "complete": task.complete, "actual_id": task.actual_id, "task_id": task.id,
             "title": task.title, "ordernumber": task.ordernumber, "datedue": dateformat, "archive": task.archive,
             "worker_name": task_worker.first_name, "worker_id": task_worker.id, "worker_email": task_worker.email,
             "date_due_in_unix": date_due_in_unix})

    taskstodisplay = sorted(taskstodisplay, key=lambda k: k['date_due_in_unix'])

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
                print("1 " + str(type(worker)))
                undonetasksl = {}
                print("1 " + str(type(worker)))
                for worker1 in workerslist:
                    from . import undonetasks
                    undonetasksl[worker1["id"]] = undonetasks(worker1["id"])
                workerslist = sorted(workerslist, key=lambda k: undonetasksl[k['id']], reverse=True)

    if search is not None:
        workerslist = [worker for worker in workerslist if
                       search.lower() in worker["name"].lower() or search.lower() in worker["email"].lower()]

    return render_template("workers.html",calendar=getword("calendar", cookie), cookie=getcookie(request), profilenav=getword("profilenav", cookie),
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
                           areyousure=getword("areyousure", cookie), chatnav=getword("chatnav", cookie),
                           moreinfo=getword("moreinfo", cookie), notdone=getword("notdone", cookie),
                           tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie),
                           notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie),
                           started=getword("started", cookie), deletefromall=getword("deletefromall", cookie),
                           workeridtext=getword("workeridtext", cookie), unarchive=getword("unarchive", cookie),
                           fullydelete=getword("fullydelete", cookie),
                           workeremailtext=getword("workeremailtext", cookie),
                           sorttypestatus=getword("sorttypestatus", cookie),
                           sorttypedate=getword("sorttypedate", cookie), sorttypetitle=getword("sorttypetitle", cookie),
                           sorttypearchive=getword("sorttypearchive", cookie), done=getword("done", cookie),
                           theme=gettheme(request))


@views.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():

    cookie = getcookie(request)

    import plotly.figure_factory as ff
    import plotly.offline as pyo

    tasks = []


    if current_user.accounttype == "boss":
        for task in Task.query.filter_by(boss_id=current_user.id).all():

            taskdue = str(task.datedue)
            taskdue = str(datetime.datetime.strptime(taskdue, "%Y-%m-%d %H:%M:%S"))
            taskdue = taskdue.split(" ||| ")[0]

            taskstart = str(task.datecreated)
            taskstart = str(datetime.datetime.strptime(taskstart, "%Y-%m-%d %H:%M:%S"))
            taskdue = taskdue.split(" ||| ")[0]

            taskworker = Worker.query.filter_by(id=task.worker_id).first()

            tasks.append({"Task": task.title + " (" + taskworker.first_name + ")", "Start": taskstart, "Finish": taskdue})
    elif current_user.accounttype == "worker":
        for task in Task.query.filter_by(worker_id=current_user.id).all():

            taskdue = str(task.datedue)
            taskdue = str(datetime.datetime.strptime(taskdue, "%Y-%m-%d %H:%M:%S"))
            taskdue = taskdue.split(" ||| ")[0]

            taskstart = str(task.datecreated)
            taskstart = str(datetime.datetime.strptime(taskstart, "%Y-%m-%d %H:%M:%S"))
            taskdue = taskdue.split(" ||| ")[0]


            tasks.append(
                {"Task": task.title, "Start": taskstart, "Finish": taskdue})

    colors = []
    for task in tasks:
        taskT = task['Task']
        start = task['Start']
        finish = task['Finish']
        if not taskT.isascii():
            taskT = translit(taskT, reversed=True)

        seed = taskT + start + finish + taskT + finish + start
        random.seed(seed)
        colors.append('#%06X' % random.randint(0, 0xFFFFFF))

    fig = ff.create_gantt(tasks, colors=colors, index_col='Task', show_colorbar=False, bar_width=0.2, height=400,
                          group_tasks=False, title=getword("taskschedule", cookie), showgrid_x=True, showgrid_y=True,
                          show_hover_fill=True)

    fig.update_layout(xaxis_title=getword("dates", cookie), yaxis_title=getword("tasks", cookie), font=dict(family='Arial', size=14, color='#333'),
        plot_bgcolor='#f8f8f8', paper_bgcolor='#f8f8f8', margin=dict(l=80, r=30, t=60, b=30),
        hoverlabel=dict(bgcolor='#FFF', font_size=14, font_family='Arial'), autosize=True)
    plot = pyo.plot(fig, output_type='div')

    return render_template("calendar.html",calendar=getword("calendar", cookie), cookie=getcookie(request), plot=plot,
                           profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie),
                           signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie),
                           workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie),
                           logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie),
                           user=current_user, idtext=getword("idtext", cookie), addworker=getword("addworker", cookie),
                           delete=getword("delete", cookie), workertext=getword("workertext", cookie),
                           addtask=getword("addtask", cookie), email=getword("email", cookie),
                           name=getword("name", cookie), selectall=getword("selectall", cookie),
                           deselectall=getword("deselectall", cookie), workermenu=getword("workermenu", cookie),
                           submit=getword("submit", cookie), selectworkers=getword("selectworkers", cookie),
                           signupemploy=getword("signupemploy", cookie), here=getword("here", cookie),
                           myfiles=getword("empmyfiles", cookie), adminpaneltext=getword("adminpaneltext", cookie),
                           addemployeebutton=getword("addemployeebutton", cookie),
                           registeryouremployee=getword("registeryouremployee", cookie),
                           addtasktext=getword("addtasktext", cookie), actiontext=getword("actiontext", cookie),
                           sorttext=getword("sorttext", cookie), sortnametext=getword("sortnametext", cookie),
                           sortemailtext=getword("sortemailtext", cookie),
                           sorttaskstext=getword("sorttaskstext", cookie),
                           currentlysorting=getword("currentlysorting", cookie), nonetext=getword("nonetext", cookie),
                           taskstext=getword("tasksnav", cookie), search=getword("search", cookie),
                           areyousure=getword("areyousure", cookie), chatnav=getword("chatnav", cookie),
                           moreinfo=getword("moreinfo", cookie), notdone=getword("notdone", cookie),
                           tasktext=getword("tasktext", cookie), statustext=getword("statustext", cookie),
                           notstarted=getword("NotStarted", cookie), completed=getword("completed", cookie),
                           started=getword("started", cookie), deletefromall=getword("deletefromall", cookie),
                           workeridtext=getword("workeridtext", cookie), unarchive=getword("unarchive", cookie),
                           fullydelete=getword("fullydelete", cookie),
                           workeremailtext=getword("workeremailtext", cookie),
                           sorttypestatus=getword("sorttypestatus", cookie),
                           sorttypedate=getword("sorttypedate", cookie), sorttypetitle=getword("sorttypetitle", cookie),
                           sorttypearchive=getword("sorttypearchive", cookie), done=getword("done", cookie),
                           theme=gettheme(request))


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

    taskstodisplay.sort(key=lambda x: x['datedue'], reverse=True)

    for task in taskstodisplay:
        if task['complete'] == "2":
            taskstodisplay.remove(task)
            taskstodisplay.append(task)

    for task in taskstodisplay:
        if task['archive'] == "1":
            taskstodisplay.remove(task)
            taskstodisplay.append(task)

    sort = request.args.get('sort')
    if sort == "date":
        taskstodisplay.sort(key=lambda x: x['datedue'])
    elif sort == "title":
        taskstodisplay.sort(key=lambda x: x['title'].lower())
    elif sort == "status":
        taskstodisplay.sort(key=lambda x: x['complete'], reverse=False)
    elif sort == "archive":
        taskstodisplay.sort(key=lambda x: x['archive'], reverse=True)

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
            task.complete = "2"
            db.session.commit()
            return redirect(url_for(oneworkerpage, id=id))
        elif typeform == 'delete':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            db.session.delete(task)
            db.session.commit()
            return redirect(url_for(oneworkerpage, id=id))
        elif typeform == 'notdone':
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            taskpost.complete = "0"
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
        elif typeform == 'started':
            taskid = request.form.get('task_id')
            task = Task.query.get(taskid)
            task.complete = "1"
            db.session.commit()
            return redirect(url_for(oneworkerpage, id=id))

    return render_template("worker.html",calendar=getword("calendar", cookie), cookie=getcookie(request), profilenav=getword("profilenav", cookie),
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
                           chatnav=getword("chatnav", cookie), workername=worker.first_name, workeremail=worker.email,
                           workeremailtext=getword("workeremailtext", cookie),
                           currentlysorting=getword("currentlysorting", cookie),
                           sorttypestatus=getword("sorttypestatus", cookie),
                           sorttypedate=getword("sorttypedate", cookie), sorttypetitle=getword("sorttypetitle", cookie),
                           sorttypearchive=getword("sorttypearchive", cookie), nonetext=getword("nonetext", cookie),
                           sorttext=getword("sorttext", cookie), sorttype=sort, theme=gettheme(request))


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
        elif typeform == "start":
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            taskpost.complete = "1"
            db.session.commit()
            return redirect(url_for('views.task', id=id))
        elif typeform == "addtocalendar":
            taskid = request.form.get('task_id')
            from .translator import addtogooglecalendar
            response = addtogooglecalendar(taskid)
            if response == "OK":
                flash("Added to Google Calendar", category="success")
            else:
                flash("Failed to add to Google Calendar", category="error")
            return redirect(url_for('views.task', id=id))
        elif typeform == "attach":
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            file = request.form.get('file')
            if "GOOGLEDOC???" not in file:
                filename = current_user.id + "_" + file
            else:
                filename = file
            if file is None or file == "" or file == " ":
                flash(getword("fileisnone", cookie), category="error")
                return redirect(url_for('views.task', id=id))
            if "GOOGLEDOC???" not in file:
                if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    attachements1 = taskpost.attachments
                    for attachement in attachements1.split("|FILESEPARATOR|"):
                        if attachement == filename:
                            flash(getword("filealreadyattached", cookie), category="error")
                            return redirect(url_for('views.task', id=id))
                    currnetattachments = taskpost.attachments
                    taskpost.attachments = currnetattachments + '|FILESEPARATOR|' + filename
                    db.session.commit()
            else:
                attachements1 = taskpost.attachments
                for attachement in attachements1.split("|FILESEPARATOR|"):
                    if attachement == filename:
                        flash(getword("filealreadyattached", cookie), category="error")
                        return redirect(url_for('views.task', id=id))
                currnetattachments = taskpost.attachments
                try:
                    taskpost.attachments = currnetattachments + '|FILESEPARATOR|' + filename
                    db.session.commit()
                    idd = file.split("GOOGLEDOC???")[1]
                    if current_user.accounttype == "boss":
                        otheruser = Worker.query.get(taskpost.worker_id)
                    else:
                        otheruser = Boss.query.get(taskpost.boss_id)
                    sharefile(idd, otheruser.email)
                except Exception as e:
                    flash("Fail", category="error")
                    return redirect(url_for('views.task', id=id))


        elif typeform == "deleteattachment":
            taskid = request.form.get('task_id')
            taskpost = Task.query.get(taskid)
            file = request.form.get('file')
            if "GOOGLEDOC???" not in file:
                filename = current_user.id + "_" + file
            else:
                filename = file
            if file is None or file == "" or file == " ":
                flash(getword("fileisnone", cookie), category="error")
                return redirect(url_for('views.task', id=id))
            attachements1 = taskpost.attachments
            attachements2 = attachements1.split("|FILESEPARATOR|")
            if len(attachements2) == 1:
                taskpost.attachments = ""
                db.session.commit()
            else:
                attachements3 = ""
                for attachement in attachements2:
                    if attachement != filename:
                        attachements3 = attachements3 + "|FILESEPARATOR|" + attachement
                taskpost.attachments = attachements3
                db.session.commit()

    datedue = taskdata.datedue
    dateformat = time.strftime("%e/%m/%Y - %R", datedue.timetuple())

    myfiles = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        file1 = file.split("_")
        if str(file1[0]) == str(current_user.id):
            myfiles.append(file)

    myfileswithoutid = []
    for file in myfiles:
        file1 = file.split("_")
        myfileswithoutid.append(file1[1])


    for file in str(current_user.googlefiles).split("|GOOGLEDOCSFILESEPARATOR|"):
        print(file)
        if file.rstrip() != "" and file is not None and file != "None":
            newfile = "GOOGLEDOC???" + file
            myfileswithoutid.append(newfile)


    attachements = taskdata.attachments
    attachements = attachements.split("|FILESEPARATOR|")

    attachements1 = []
    for attachement in attachements:
        if attachement != "":
            attachements1.append(attachement)

    return render_template("task.html",calendar=getword("calendar", cookie), cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie),
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
                           chatnav=getword("chatnav", cookie), comment=getword("comment", cookie), myfiles=myfiles,
                           myfileswithoutid=myfileswithoutid, attachements=attachements1, theme=gettheme(request))


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

    return render_template("contact.html",calendar=getword("calendar", cookie), cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user,
                           contactus=getword("contactus", cookie), contactusmessage=getword("contactusmessage", cookie),
                           contactname=getword("contactname", cookie), contactemail=getword("contactemail", cookie),
                           contactname2=getword("contactname2", cookie), contactemail2=getword("contactemail2", cookie),
                           name=getword("name", cookie), email=getword("email", cookie),
                           message=getword("message", cookie), chatnav=getword("chatnav", cookie),
                           theme=gettheme(request))


@views.route("/cookies-disabled", methods=["GET"])
def cookies_disabled():
    return render_template("cookies_disabled.html", cookie=getcookie(request), user=current_user)


@views.route("/privacy", methods=["GET"])
def privacy():
    cookie = getcookie(request)

    return render_template("privacy.html",calendar=getword("calendar", cookie), cookie=getcookie(request), user=current_user,
                           privacypolicytitle=getword("privacypolicytitle", cookie),
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
                           privacypolicytext14=getword("privacypolicytext14", cookie),
                           chatnav=getword("chatnav", cookie), homenav=getword("homenav", cookie),
                           loginnav=getword("loginnav", cookie), profilenav=getword("profilenav", cookie),
                           signupnav=getword("signupnav", cookie), workersnav=getword("workersnav", cookie),
                           tasksnav=getword("tasksnav", cookie), theme=gettheme(request))


@views.route("/videochat", methods=["GET", "POST"])
@login_required
def videochat():
    from website.token.RtcTokenBuilder import RtcTokenBuilder

    username = current_user.first_name

    if not username.isascii():
        username = translit(username, reversed=True)

    username1 = username.rstrip()

    randomid = current_user.first_name
    randomid = randomid.replace(" ", "")
    randomid = randomid.lower()
    randomid = randomid + "-|-" + str(current_user.number)

    if not randomid.isascii():
        randomid = translit(randomid, reversed=True)

    current_unix_timestamp = int(time.time())
    hours_from_now = current_unix_timestamp + 24 * 60 * 60

    token = RtcTokenBuilder.buildTokenWithUid("8b975af4453648a3b932f332d4501db8", "6c4beaa4ecf54e8b9d8ed547fd2c3d76",
                                              "Hey", randomid, "1", hours_from_now)

    print(token)

    return render_template("videochat.html", cookie=getcookie(request), user=current_user, username=username1,
                           randomid=randomid, token=token)


@views.route("/getname/videochat/<id>", methods=["GET", "POST"])
@login_required
def getname(id):
    username = id
    firstpart = username.split("-|-")[0]
    secondpart = username.split("-|-")[1]
    if len(username.split("-|-")) > 2:
        return jsonify({"status": "error", "message": "Invalid username"})
    else:
        user = Worker.query.filter_by(number=secondpart).first()
        if user is None:
            user = Boss.query.filter_by(number=secondpart).first()
            if user is None:
                return jsonify({"status": "error", "message": "Invalid username"})

        name = user.first_name
        if not name.isascii():
            name = translit(name, reversed=True)

        return jsonify({"status": "success", "name": name, "id": user.id})
