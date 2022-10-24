from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFError
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from .mailsender import sendregisterationemail, sendregisterationemailboss
import requests


from website import CAPTCHA1
from . import db
from .models import Worker, Boss
import uuid
from .translator import getword, loadtime

auth = Blueprint('auth', __name__)
global csrfg

class StatusDenied(Exception):
    print("StatusDenied Exception")


@auth.errorhandler(StatusDenied)
def redirect_on_status_denied1(error):
    flash("")
    return render_template("maintenance.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie)), 403




def checkmaintenance():
    pass
    # try:
    #     r = requests.get("https://api.npoint.io/fdd18b346a9f50481a65")
    #     if r.json()["status"] == "maintain":
    #         print("maintenance 1")
    #         raise StatusDenied()
    #     else:
    #         pass
    # except Exception as e:
    #     print(e)
    #     raise StatusDenied()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    checkmaintenance()
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        if request.method == 'POST':
            accounttype = request.form.get('accounttype')
            email = request.form.get('email')
            password = request.form.get('password')

            if accounttype == 'worker':
                user = Worker.query.filter_by(email=email).first()
            else:
                user = Boss.query.filter_by(email=email).first()

            if user:
                if check_password_hash(user.password, password):
                    flash(getword("loggedinsuccess", cookie), category='success')
                    login_user(user, remember=True)
                    if accounttype == 'worker':
                        return redirect(url_for('views.boss'))
                    else:
                        return redirect(url_for('views.home'))
                else:
                    flash(getword("incorrectpass", cookie), category='error')
            else:
                flash(getword("emailnotfound", cookie), category='error')

    return render_template("login.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie), user=current_user,
                           emailtext=getword("email", cookie),
                           passwordtext=getword("password", cookie),
                           logintext=getword("login", cookie),
                           enterpassword=getword("enterpassword", cookie),
                           enteremail=getword("enteremail", cookie),
                           registerhere=getword("registerhere", cookie),
                           notregistered=getword("notregistered", cookie))


@auth.route('/logout')
@login_required
def logout():
    checkmaintenance()
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'
    if current_user.is_authenticated:
        logout_user()
        flash(getword("loggedoutsuccess", cookie), category='success')
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    checkmaintenance()
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.is_authenticated:
        if current_user.accounttype == 'worker' and current_user.boss_id is None:
            return redirect(url_for('views.boss'))
        else:
            return redirect(url_for('views.home'))
    captcha = CAPTCHA1.create()
    if request.method == 'POST':
        accounttype = request.form.get('accounttype')
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if c_hash is None:
            return render_template("hash_error.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie), user=current_user)

        if not CAPTCHA1.verify(c_text, c_hash):
            flash(getword("captchawrong", cookie), category='error')
            return redirect(url_for('auth.sign_up'))

        email = request.form.get('email')


        try:
            v = validate_email(email, check_deliverability=True)
            email = v["email"]
            parts1 = email.split('@')
            if parts1[1] == "tasklify.me":
                flash(getword("tasklifymedomainnotallowed", cookie), category='error')
                return redirect(url_for('auth.sign_up'))
        except EmailNotValidError as e:
            flash(e, category='error')
            return redirect(url_for('auth.sign_up'))



        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if accounttype == 'worker':
            user = Worker.query.filter_by(email=email).first()
        elif accounttype == 'boss':
            user = Boss.query.filter_by(email=email).first()
        else:
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
            if accounttype == 'worker':
                key = uuid.uuid4().hex
                new_user = Worker(email=email, first_name=first_name,
                                  password=generate_password_hash(password1, method='sha256'), accounttype="worker", registrationid=key)
            elif accounttype == 'boss':
                new_user = Boss(email=email, first_name=first_name,
                                password=generate_password_hash(password1, method='sha256'), accounttype="boss")
            else:
                flash("Error. Type not selected.", category='error')
                return redirect(url_for('auth.sign_up'))

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(getword("accountcreated", cookie), category='success')
            if accounttype == 'worker':
                sendregisterationemail(email, first_name, current_user.registrationid)
                return redirect(url_for('views.boss'))
            else:
                sendregisterationemailboss(email, first_name)
                return redirect(url_for('views.home'))


    return render_template("sign_up.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie), user=current_user, captcha=captcha,
                           emailtext=getword("email", cookie),
                           nametext=getword("name", cookie),
                           passwordtext=getword("password", cookie),
                           passwordconfirm=getword("cnewpassword", cookie),
                           submit=getword("submit", cookie),
                           firstandlast=getword("firstandlast", cookie),
                           signup=getword("signup", cookie),
                           enteremail=getword("enteremail", cookie),
                           alreadyhaveaccount=getword("alreadyhaveaccount", cookie),
                           loginhere=getword("loginhere", cookie), databeingproccessed=getword("databeingproccessed", cookie))

@auth.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    checkmaintenance()
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.is_authenticated and current_user.accounttype == 'boss':
        if current_user.workers:
            flash(getword("youhaveworkerscannotdelete", cookie), category='error')
            return redirect(url_for('views.home'))

    if request.method == 'POST':
        checkbox = request.form.get('confirm')
        password = request.form.get('password')
        email = current_user.email
        if checkbox == 'on':
            if current_user.accounttype == 'worker':
                user = Worker.query.filter_by(email=email).first()
            else:
                user = Boss.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    db.session.delete(user)
                    db.session.commit()
                    flash(getword("accontdeletesuccess", cookie), category='success')
                    return redirect(url_for('auth.login'))
                else:
                    flash(getword("incorrectpass", cookie), category='error')
        else:
            flash(getword("youmustconfirmdelete", cookie), category='error')


    return render_template("delete_account.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie), user=current_user,
                           deleteaccount=getword("deleteaccount", cookie),
                           confirmtext=getword("confirmdelete", cookie),
                           password=getword("password", cookie),
                           enterpassword=getword("enterpassword", cookie))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    checkmaintenance()
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'
    captcha = CAPTCHA1.create()
    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        password3 = request.form.get('password3')
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if c_hash is None:
            return render_template("hash_error.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie), user=current_user)

        confirm = request.form.get('confirm')
        email = current_user.email
        if current_user.accounttype == 'worker':
            user = Worker.query.filter_by(email=email).first()
        else:
            user = Boss.query.filter_by(email=email).first()
        if not CAPTCHA1.verify(c_text, c_hash):
            flash(getword("captchawrong", cookie), category='error')
            return redirect(url_for('auth.change_password'))

        if confirm != 'on':
            flash(getword("mustconfirmchangepassword", cookie), category='error')
            return redirect(url_for('auth.change_password'))

        if user:
            if check_password_hash(user.password, password1):
                if password2 != password3:
                    flash(getword("passwordsdontmatch", cookie), category='error')
                elif len(password2) < 8:
                    flash(getword("passwordtooshort", cookie), category='error')
                else:
                    user.password = generate_password_hash(password2, method='sha256')
                    db.session.commit()
                    flash(getword("passwordchangedsuccess", cookie), category='success')
                    return redirect(url_for('views.home'))
            else:
                flash(getword("incorrectpass", cookie), category='error')

    return render_template("change_password.html", profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie), user=current_user, captcha=captcha,
                           changepassword=getword("changepassword", cookie),
                           oldpassword=getword("oldpassword", cookie),
                           newpassword=getword("newpassword", cookie),
                           cnewpassword=getword("cnewpassword", cookie),
                           confirmtext=getword("confirm", cookie),
                           enterpassword=getword("enterpassword", cookie))


@auth.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description, user=current_user), 400
