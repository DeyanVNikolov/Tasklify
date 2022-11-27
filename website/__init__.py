import os
import os.path as op
from os import path

from flask import Flask, render_template
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import LoginManager, current_user
from flask_simple_captcha import CAPTCHA
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_limiter import Limiter
from flask import jsonify
from flask_limiter.util import get_remote_address
from website.translator import getword
from dotenv import load_dotenv

# check if server or local
load_dotenv(".env")

print("Starting up...")

print("_____")
print(os.getenv("SQL_PASSWORD"))
print(os.getenv("SQL_USER"))
print(os.getenv("SQL_HOST"))
print(os.getenv("SQL_DBNAME"))
print("_____")


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://doadmin:{os.getenv("SQL_PASSWORD")}@{os.getenv("SQL_HOST")}:25060/defaultdb'
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    # pooling timeout
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_CAPTCHA_KEY'] = 'wMmeltW4mhwidorQRli6Oijuhygtfgybunxx9VPXldz'
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = "./translations"
    app.config['LANGUAGES'] = {'en': 'English', 'de': 'Deutsch'}
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = 'website/static/uploads'

    global CAPTCHA1
    CAPTCHA1 = CAPTCHA(config=app.config)
    global csrfg
    csrfg = CSRFProtect(app)
    csrfg.init_app(app)
    db.init_app(app)
    CAPTCHA1.init_app(app)
    toolbar = DebugToolbarExtension(app)
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'


    app.jinja_env.globals.update(getword=getword)
    app.jinja_env.globals.update(undonetasks=undonetasks)
    global limiter

    limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per minute"], storage_uri="memory://", )



    from .views import views
    from .auth import auth
    # from .payments import payments

    # csrfg.exempt(payments)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    # app.register_blueprint(payments, url_prefix='/')

    from .models import Worker as WorkerModel, Boss as BossModel, Task as TaskModel

    class MyModelView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated:
                if current_user.accounttype == "boss" and current_user.additionalpermissions == "ADMIN":
                    return current_user.is_authenticated

        column_searchable_list = ['email', 'id']
        column_list = ['id', 'email', 'first_name', "password", "boss_id", "accounttype", "registrationid", "additionalpermissions", "tasks", "user_id"]


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

    admin = Admin(app, name='Dashboard', template_mode='bootstrap3', index_view=MyAdminIndexView(url="/internal/admin-dashboard"), url="/internal/admin-dashboard")
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
        return render_template('notfound.html'), 404

    @app.errorhandler(429)
    def too_many_reqeusts(e):
        return jsonify({"error": "Too many requests"}), 429

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('forbidden.html'), 403


    return app


def create_database(app):
    db.create_all(app=app)
    print('Created Database!')

def undonetasks():
    from .models import Task
    if current_user.accounttype == "worker":
        print(current_user.first_name)
        print(current_user.id)
        total = Task.query.filter_by(worker_id=current_user.id).filter_by(complete="0").count() + Task.query.filter_by(worker_id=current_user.id).filter_by(complete="1").count()
        return total





app = create_app()

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
