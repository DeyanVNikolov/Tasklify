import os
import uuid

from email_validator import validate_email
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import session
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFError
from werkzeug.security import generate_password_hash, check_password_hash

from website import CAPTCHA1
from . import db
from .mailsender import sendregisterationemail, sendregisterationemailboss
from .models import Worker, Boss
from .translator import gettheme
from .translator import getword
from .twofactor import verifyfactor, verifyuser

auth = Blueprint('auth', __name__)
global csrfg


def getcookie(request):
    if 'locale' in request.cookies:
        return request.cookies.get('locale')
    else:
        return 'en'


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Вземаме какъв е езика на потребителя
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    # Проверяваме дали потребителя е логнат
    if current_user.is_authenticated:
        # Ако е логнат, го пренасочваме към началната страница
        return redirect(url_for('views.home'))
    else:
        # Ако не е логнат, показваме формата за логване
        if request.method == 'POST':
            # Вземаме данните от формата
            email = request.form.get('email')
            password = request.form.get('password')

            # search for email in database
            user = Worker.query.filter_by(email=email).first()
            if not user:
                user = Boss.query.filter_by(email=email).first()
            if not user:
                flash(getword("emailnotfound", cookie), category='error')
                return redirect(url_for('auth.login'))
            # Проверяваме дали потребителя съществува
            if user:
                # Проверяваме дали профила е ДЕМО
                if user.id.split("-")[0] != "DEMO":
                    # Проверяваме дали паролата е вярна
                    if check_password_hash(user.password, password):
                        # Ако е вярна, логваме потребителя
                        # use rstrip
                        if user.factor is not None:
                            if user.factor.rstrip() != "":
                                session['email'] = email
                                session['password'] = password
                                user.twofactorneeded = "1"
                                return redirect(url_for('auth.two_factor'))
                        else:
                            flash(getword("loggedinsuccess", cookie), category='success')
                            login_user(user, remember=False)
                        if user.accounttype == 'worker':
                            return redirect(url_for('views.boss'))
                        else:
                            return redirect(url_for('views.home'))
                    else:
                        # Ако не е вярна, показваме съобщение за грешка
                        flash(getword("incorrectpass", cookie), category='error')
                else:
                    # Ако е ДЕМО, показваме съобщение за грешка
                    flash(getword("demoaccount", cookie), category='error')
            else:
                # Ако потребителя не съществува, показваме съобщение за грешка
                flash(getword("emailnotfound", cookie), category='error')

    # Показваме формата за логване
    return render_template("login.html",cookie=getcookie(request), profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie),
                           signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie),
                           workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie),
                           logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie),
                           user=current_user, emailtext=getword("email", cookie),
                           passwordtext=getword("password", cookie), logintext=getword("login", cookie),
                           enterpassword=getword("enterpassword", cookie), enteremail=getword("enteremail", cookie),
                           registerhere=getword("registerhere", cookie), notregistered=getword("notregistered", cookie),
                           worker=getword("worker", cookie), boss=getword("boss", cookie),
                           loginwith=getword("loginwith", cookie), signinwithgithub=getword("signinwithgithub", cookie),
                           signinwithgoogle=getword("signinwithgoogle", cookie),
                           signinwithfacebook=getword("signinwithfacebook", cookie), theme=gettheme(request))


@auth.route("/2fa", methods=['GET', 'POST'])
def two_factor():

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if session.get("email") is None or session.get("password") is None:
        flash("Token mismatch, make sure your cookies are enabled", category="error")
        return redirect(url_for('auth.logout'))

    if request.method == 'POST':
        if request.form.get("typeform") == "submit2fa":
            if request.form.get("code") is not None and request.form.get("code").rstrip() != "":
                if len(request.form.get("code").rstrip()) < 3 or len(
                        request.form.get("code").rstrip()) > 6 or not request.form.get(
                        "code").rstrip().isdigit() or len(request.form.get("code").rstrip()) <= 1:
                    flash("Invalid code", category="error")
                    return redirect(url_for('auth.two_factor'))
                user = Worker.query.filter_by(email=session.get("email")).first()
                if user is None:
                    user = Boss.query.filter_by(email=session.get("email")).first()
                    if user is None:
                        flash("Token mismatch, make sure your cookies are not tampered with", category="error")
                        return redirect(url_for('auth.logout'))
                verification = verifyuser(user.id, user.id.replace("-", ""), request.form.get("code").rstrip())
                if verification != "403":
                    if verification.status == "approved":
                        newuser = Worker.query.filter_by(email=session.get("email")).first()
                        if newuser is None:
                            newuser = Boss.query.filter_by(email=session.get("email")).first()
                            if newuser is None:
                                flash("Token mismatch, make sure your cookies are not tampered with", category="error")
                                return redirect(url_for('auth.logout'))
                        if check_password_hash(newuser.password, session.get("password")):
                            flash(getword("loggedinsuccess", cookie), category='success')
                            session.pop("email")
                            session.pop("password")
                            newuser.twofactorneeded = "1"
                            login_user(newuser, remember=False)
                            if newuser.accounttype == 'worker':
                                return redirect(url_for('views.boss'))
                            else:
                                return redirect(url_for('views.home'))
                    else:
                        flash("Invalid code", category="error")
                        print("invalid code")
                        return redirect(url_for('auth.two_factor'))
            else:
                flash("Invalid code", category="error")
                return redirect(url_for('auth.two_factor'))

    return render_template("2fa.html",cookie=getcookie(request), profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie),
                           signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie),
                           workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie),
                           logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie),
                           user=current_user, emailtext=getword("email", cookie),
                           passwordtext=getword("password", cookie), logintext=getword("login", cookie),
                           enterpassword=getword("enterpassword", cookie), enteremail=getword("enteremail", cookie),
                           registerhere=getword("registerhere", cookie), notregistered=getword("notregistered", cookie),
                           worker=getword("worker", cookie), boss=getword("boss", cookie),
                           loginwith=getword("loginwith", cookie), signinwithgithub=getword("signinwithgithub", cookie),
                           signinwithgoogle=getword("signinwithgoogle", cookie),
                           signinwithfacebook=getword("signinwithfacebook", cookie), theme=gettheme(request),
                           logout=getword("logout", cookie), enter2fa=getword("enter2fa", cookie),
                           submit=getword("submit", cookie), gate2fa=getword("gate2fa", cookie))


@auth.route("/2fa/logout", methods=['GET', 'POST'])
def logout_two_factor():
    print("logout")
    if session.get("email") is not None:
        print("email")
        session.pop("email")
    if session.get("password") is not None:
        print("password")
        session.pop("password")
    logout_user()

    return redirect(url_for('auth.login'))


@auth.route("/2fa/enable", methods=['GET', 'POST'])
@login_required
def enable_two_factor():
    from .twofactor import generate_new_factor

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.factor is not None:
        if current_user.factor.rstrip() != "":
            flash("2FA already enabled", category='error')
            return redirect(url_for('views.home'))

    uuid = current_user.id
    # remove dashes, hex
    uuid = uuid.replace("-", "")

    old_factor = request.form.get("old_factor")

    print("OLD:" + str(old_factor))

    if old_factor is None or old_factor.rstrip() == "":
        new_factor = generate_new_factor(current_user.first_name, current_user.id.replace("-", ""), current_user.id)

    if request.method == "POST":
        if request.form.get("typeform") == "Confirm":
            if old_factor is not None and old_factor.rstrip() != "":
                current_user.factor = old_factor
                db.session.commit()
                return redirect(url_for('auth.confirm_two_factor', factor=old_factor))

    return render_template("enable2fa.html",cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user, emailtext=getword("email", cookie),
                           passwordtext=getword("password", cookie), logintext=getword("login", cookie),
                           enterpassword=getword("enterpassword", cookie), enteremail=getword("enteremail", cookie),
                           registerhere=getword("registerhere", cookie), notregistered=getword("notregistered", cookie),
                           worker=getword("worker", cookie), boss=getword("boss", cookie),
                           loginwith=getword("loginwith", cookie), signinwithgithub=getword("signinwithgithub", cookie),
                           signinwithgoogle=getword("signinwithgoogle", cookie),
                           signinwithfacebook=getword("signinwithfacebook", cookie), theme=gettheme(request), uuid=uuid,
                           factor=new_factor.sid)


@auth.route("/2fa/confirm/<factor>", methods=['GET', 'POST'])
@login_required
def confirm_two_factor(factor):

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    uuid = current_user.id.replace("-", "")

    if current_user.factor != factor:
        flash("Token mismatch", category='error')
        return redirect(url_for('views.home'))

    if request.method == "POST" and request.form.get("typeform") == "Code":
        print(request.form.get("code"))
        verification = verifyfactor(current_user.id, uuid, request.form.get("code"))
        if verification == "403":
            flash("2FA failed. Try again", category='error')
            # delete file in static/qr
            current_user.factor = None
            db.session.commit()
            os.remove(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/qr/" + uuid + uuid + uuid + ".png"))
            return redirect(url_for('views.home'))

        print(verification.status)

        if verification.status == "verified":
            flash("2FA enabled", category='success')
            return redirect(url_for('views.home'))
        else:
            flash("2FA failed. Try again", category='error')
            current_user.factor = None
            db.session.commit()
            os.remove(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/qr/" + uuid + uuid + uuid + ".png"))

            return redirect(url_for('views.home'))

    return render_template("confirm2fa.html",cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user, emailtext=getword("email", cookie),
                           passwordtext=getword("password", cookie), logintext=getword("login", cookie),
                           enterpassword=getword("enterpassword", cookie), enteremail=getword("enteremail", cookie),
                           registerhere=getword("registerhere", cookie), notregistered=getword("notregistered", cookie),
                           worker=getword("worker", cookie), boss=getword("boss", cookie),
                           loginwith=getword("loginwith", cookie), signinwithgithub=getword("signinwithgithub", cookie),
                           signinwithgoogle=getword("signinwithgoogle", cookie),
                           signinwithfacebook=getword("signinwithfacebook", cookie), theme=gettheme(request), uuid=uuid)


@auth.route("/2fa/disable", methods=['GET', 'POST'])
@login_required
def disable_two_factor():

    current_user.factor = None
    db.session.commit()
    flash("2FA disabled", category='success')
    return redirect(url_for('views.profileset2fa'))


@auth.route('/logout')
@login_required
def logout():
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
            return render_template("hash_error.html",cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                                   loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                                   tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                                   adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                                   homenav=getword("homenav", cookie), user=current_user)

        session['emailb'] = request.form.get('email')
        session['passwordb'] = request.form.get('password1')
        session['accounttypeb'] = accounttype
        session['nameb'] = request.form.get('firstName')

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
        except Exception as e:
            flash(str(e), category='error')
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
                key = uuid.uuid4().hex[:12]
                new_user = Worker(email=email, first_name=first_name,
                                  password=generate_password_hash(password1, method='sha256'), accounttype="worker",
                                  registrationid=key)
            elif accounttype == 'boss':
                new_user = Boss(email=email, first_name=first_name,
                                password=generate_password_hash(password1, method='sha256'), accounttype="boss")
            else:
                flash("Error. Type not selected.", category='error')
                return redirect(url_for('auth.sign_up'))

            db.session.add(new_user)
            db.session.commit()
            session.clear()
            login_user(new_user, remember=True)
            flash(getword("accountcreated", cookie), category='success')
            if accounttype == 'worker':
                sendregisterationemail(email, first_name, current_user.registrationid)
                return redirect(url_for('views.boss'))
            else:
                sendregisterationemailboss(email, first_name)
                return redirect(url_for('views.home'))

    emailb = session.get('emailb', None)
    passwordb = session.get('passwordb', None)
    accounttypeb = session.get('accounttypeb', None)
    nameb = session.get('nameb', None)

    return render_template("sign_up.html",cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user, captcha=captcha,
                           emailtext=getword("email", cookie), nametext=getword("name", cookie),
                           passwordtext=getword("password", cookie), passwordconfirm=getword("cnewpassword", cookie),
                           submit=getword("submit", cookie), firstandlast=getword("firstandlast", cookie),
                           signup=getword("signup", cookie), enteremail=getword("enteremail", cookie),
                           alreadyhaveaccount=getword("alreadyhaveaccount", cookie),
                           loginhere=getword("loginhere", cookie),
                           databeingproccessed=getword("databeingproccessed", cookie),
                           signupas=getword("signupas", cookie), worker=getword("worker", cookie),
                           boss=getword("boss", cookie), signupwith=getword("signupwith", cookie), emailb=emailb,
                           passwordb=passwordb, acctypeb=accounttypeb, nameb=nameb,
                           signinwithgithub=getword("signinwithgithub", cookie),
                           signinwithfacebook=getword("signinwithfacebook", cookie),
                           signinwithgoogle=getword("signinwithgoogle", cookie), theme=gettheme(request))


@auth.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():

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

    return render_template("delete_account.html",cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user,
                           deleteaccount=getword("deleteaccount", cookie), confirmtext=getword("confirmdelete", cookie),
                           password=getword("password", cookie), enterpassword=getword("enterpassword", cookie),
                           chatnav=getword("chatnav", cookie), theme=gettheme(request))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():

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
            return render_template("hash_error.html",cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                                   loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                                   tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                                   adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                                   homenav=getword("homenav", cookie), user=current_user,
                                   chatnav=getword("chatnav", cookie))

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

    return render_template("change_password.html",cookie=getcookie(request), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user, captcha=captcha,
                           changepassword=getword("changepassword", cookie), oldpassword=getword("oldpassword", cookie),
                           newpassword=getword("newpassword", cookie), cnewpassword=getword("cnewpassword", cookie),
                           confirmtext=getword("confirm", cookie), enterpassword=getword("enterpassword", cookie),
                           chatnav=getword("chatnav", cookie), theme=gettheme(request))


@auth.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description, user=current_user), 400
