import datetime
import os
import os.path as op
from os import path

import requests
from flask import Flask, render_template, redirect, url_for, flash
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import LoginManager, current_user, logout_user
from .captchahandler.captchahandler import CAPTCHA
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_limiter import Limiter
from flask import jsonify, request
from flask_limiter.util import get_remote_address
from website.translator import getword
from dotenv import load_dotenv
from flask import session
from flask_session import Session

load_dotenv(".env")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

db = SQLAlchemy()
DB_NAME = "database.db"


def getofficialmessage():
    message = requests.get("https://pastebin.com/raw/vzCrN1Z5")
    if message.json()['status'] != "None":
        return message.json()['message']['en']
    else:
        return None


def getofficialmessagebg():
    message = requests.get("https://pastebin.com/raw/vzCrN1Z5")
    if message.json()['status'] != "None":
        return message.json()['message']['bg']
    else:
        return None


def getofficialmessagefr():
    message = requests.get("https://pastebin.com/raw/vzCrN1Z5")
    if message.json()['status'] != "None":
        return message.json()['message']['fr']
    else:
        return None


def getofficialmessagees():
    message = requests.get("https://pastebin.com/raw/vzCrN1Z5")
    if message.json()['status'] != "None":
        return message.json()['message']['es']
    else:
        return None


def getofficialmessagede():
    message = requests.get("https://pastebin.com/raw/vzCrN1Z5")
    if message.json()['status'] != "None":
        return message.json()['message']['de']
    else:
        return None


def getofficialmessageru():
    message = requests.get("https://pastebin.com/raw/vzCrN1Z5")
    if message.json()['status'] != "None":
        return message.json()['message']['ru']
    else:
        return None


def getdocumentname(id):
    url = f'https://docs.googleapis.com/v1/documents/{id}?fields=title'
    headers = {'Authorization': f'Bearer {current_user.google_access_token}'}
    response = requests.get(url, headers=headers)
    document_name = response.json()['title']

    return document_name


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '234e34f6-cca4-40d9-8387-304149e6e8e5'
    # mysql
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'mysql://doadmin:{os.getenv("SQL_PASSWORD")}@{os.getenv("SQL_HOST")}:25060/defaultdb'
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_CAPTCHA_KEY'] = 'wMmeltW4mhwidorQRli6Oijuhygtfgybunxx9VPXldz'
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = "./translations"
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = 'ugc/uploads'
    app.config['PFP_UPLOADS'] = 'static/pfp'
    app.config['GOOGLE_CLIENT_ID'] = "305802211949-0ca15pjp0ei2ktpsqlphhgge4vfdgh82.apps.googleusercontent.com"
    app.secret_key = '234e34f6-cca4-40d9-8387-304149e6e8e5'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(seconds=3600)

    global CAPTCHA1
    CAPTCHA1 = CAPTCHA(config=app.config)
    global csrfg
    csrfg = CSRFProtect(app)
    csrfg.init_app(app)
    db.init_app(app)
    CAPTCHA1.init_app(app)
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'

    app.jinja_env.globals.update(getword=getword)
    app.jinja_env.globals.update(undonetasks=undonetasks)
    global limiter

    SEESION_TYPE = "redis"
    app.config.from_object(__name__)
    Session(app)

    limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per minute"], storage_uri="memory://", )

    from .views import views
    from .auth import auth
    from .addtabs import addtabs
    from .fileshandler import fileshandler
    from .activationhandler import activationhandler
    from .externalcallback import externalcallback
    from .chathandler import chathandler

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(addtabs, url_prefix='/')
    app.register_blueprint(fileshandler, url_prefix='/')
    app.register_blueprint(activationhandler, url_prefix='/')
    app.register_blueprint(externalcallback, url_prefix='/')
    app.register_blueprint(chathandler, url_prefix='/')
    csrfg.exempt(externalcallback)
    limiter.limit("200 per minute")(chathandler)

    app.jinja_env.globals.update(getofficialmessage=getofficialmessage)
    app.jinja_env.globals.update(getofficialmessagebg=getofficialmessagebg)
    app.jinja_env.globals.update(getofficialmessagees=getofficialmessagees)
    app.jinja_env.globals.update(getofficialmessageru=getofficialmessageru)
    app.jinja_env.globals.update(getofficialmessagefr=getofficialmessagefr)
    app.jinja_env.globals.update(getofficialmessagede=getofficialmessagede)
    app.jinja_env.globals.update(getdocumentname=getdocumentname)

    from .models import Worker as WorkerModel, Boss as BossModel, Task as TaskModel

    class MyModelView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated:
                if current_user.accounttype == "boss" and current_user.additionalpermissions == "ADMIN":
                    return current_user.is_authenticated

        column_searchable_list = ['email', 'id']
        column_list = ['id', 'email', 'first_name', "password", "boss_id", "accounttype", "registrationid",
                       "additionalpermissions", "tasks"]

    class TaskView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated:
                if current_user.accounttype == "boss" and current_user.additionalpermissions == "ADMIN":
                    return current_user.is_authenticated

        column_searchable_list = ['id', 'worker_id', 'boss_id']
        column_list = ["id", "title", "task", "worker_id", "boss_id"]

    class MyAdminIndexView(AdminIndexView):
        def is_accessible(self):
            if current_user.is_authenticated:
                if current_user.accounttype == "boss" and current_user.additionalpermissions == "ADMIN":
                    return current_user.is_authenticated

        def is_visible(self):
            return False

    class staticfiles(FileAdmin):
        def is_accessible(self):
            if current_user.is_authenticated:
                if current_user.accounttype == "boss" and current_user.additionalpermissions == "ADMIN":
                    return current_user.is_authenticated

    admin = Admin(app, name='Dashboard', template_mode='bootstrap3',
                  index_view=MyAdminIndexView(url="/internal/admin-dashboard"), url="/internal/admin-dashboard")
    path = op.join(op.dirname(__file__), 'static')

    admin.add_view(MyModelView(WorkerModel, db.session))
    admin.add_view(MyModelView(BossModel, db.session))
    admin.add_view(TaskView(TaskModel, db.session))
    admin.add_view(staticfiles(path, name='Static Files'))
    admin.add_link(MenuLink(name='Home', category='', url="/"))
    admin.add_link(MenuLink(name='Logout', category='', url="/auth/logout"))

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        if WorkerModel.query.get(id):
            return WorkerModel.query.get(id)
        elif BossModel.query.get(id):
            return BossModel.query.get(id)

    @app.errorhandler(404)
    def page_not_found(e):
        # determine wether the rquest is coming from browser or api or console
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"error": "404 Not Found"}), 404
        else:
            return render_template('notfound.html'), 404

    @app.errorhandler(429)
    def too_many_reqeusts(e):
        return """

    <center><b>TOO MANY REQUESTS -- 100 / PER MINUTE ALLOWED</b></center>

    """, 429

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('forbidden.html'), 403

    return app


global first_time
first_time = False


def create_database(app):
    global first_time
    if not first_time:
        first_time = True
        print("Connecting to Database")
        try:
            db.create_all(app=app)
        except Exception as e:
            print(e)
            exit()
        print("Connection Success")


def undonetasks(id=None):
    from .models import Task
    if not id or id is None or id == "":
        if current_user.accounttype == "worker":
            total = Task.query.filter_by(worker_id=current_user.id).filter_by(complete="0",
                                                                              archive="0").count() + Task.query.filter_by(
                worker_id=current_user.id).filter_by(complete="1", archive="0").count()
            return total
    else:
        total = Task.query.filter_by(worker_id=id).filter_by(complete="0", archive="0").count() + Task.query.filter_by(
            worker_id=id).filter_by(complete="1", archive="0").count()
        return total


app = create_app()


@app.before_request
def before_request():
    # if user is trying to access /uplaoded_file/* or /static/* ignore the rest of the code.
    if request.path.startswith("/static") or request.path.startswith("/uploaded_file") or request.path.startswith("/messageget"):
        return

    if request.path == "/banned":
        if current_user.is_authenticated:
            if current_user.banned == "0":
                return redirect(url_for('views.home'))
        return

    if current_user.is_authenticated:
        if current_user.banned == "1":
            return redirect(url_for('views.banned'))

        if current_user.googleauthed == "1" and current_user.google_access_token is not None and current_user.google_refresh_token is not None:
            url = 'https://www.googleapis.com/oauth2/v1/tokeninfo'
            params = {'access_token': current_user.google_access_token}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print("Valid Google Access Token")
            else:
                print("Invalid Google Access Token")
                # The access token is invalid, refresh it with the refresh token
                url = 'https://oauth2.googleapis.com/token'
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                data = {'client_id': '305802211949-0ca15pjp0ei2ktpsqlphhgge4vfdgh82.apps.googleusercontent.com',
                        'client_secret': os.getenv("GOOGLE_SECRET"), 'refresh_token': current_user.google_refresh_token,
                        'grant_type': 'refresh_token'}
                response = requests.post(url, headers=headers, data=data)
                if response.status_code == 200:
                    response_data = response.json()
                    access_token = response_data['access_token']
                    current_user.google_access_token = access_token
                    db.session.commit()
                    return redirect(url_for('views.home'))
                else:
                    flash("Please re-authenticate with Google", category="error")
                    logout_user()
                    return redirect(url_for('auth.login'))

    if session.get('email') is not None:
        from .models import Worker, Boss
        user = Worker.query.filter_by(email=session['email']).first()
        if user is None:
            user = Boss.query.filter_by(email=session['email']).first()
            if user is None:
                pass
            else:
                if user.twofactorneeded == "0":
                    if request.path != "/auth/2fa" and not request.path.startswith("/static/"):
                        if request.path != "/auth/2fa/logout":
                            return redirect(url_for('auth.two_factor'))
        else:
            if user.twofactorneeded == "0":
                if request.path != "/auth/2fa" and not request.path.startswith("/static/"):
                    if request.path != "/auth/2fa/logout":
                        return redirect(url_for('auth.two_factor'))


@app.template_filter('split')
def split_filter(s, delimiter):
    return s.split(delimiter)
