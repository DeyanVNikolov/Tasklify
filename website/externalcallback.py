import os
import os
import time
import uuid

import requests
from dotenv import load_dotenv
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask import abort
from flask import current_app as app
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash

from . import db
from .mailsender import sendregisterationemail, sendregisterationemailboss
from .models import Worker, Boss
from .translator import getword

externalcallback = Blueprint('externalcallback', __name__)
load_dotenv()
check_url = "https://oauth2.googleapis.com/tokeninfo?id_token="


@externalcallback.route('/googlecallback', methods=['GET', 'POST'])
def googlelogin():
    print(request.method)
    if request.method == 'GET':
        credentials = request.args.get('code')
        if not credentials:
            abort(403)

        token_endpoint = 'https://oauth2.googleapis.com/token'
        params = {'code': credentials, 'client_id': "305802211949-0ca15pjp0ei2ktpsqlphhgge4vfdgh82.apps.googleusercontent.com",
                  'client_secret': "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", 'redirect_uri': "https://127.0.0.1:5000/googlecallback",
            'grant_type': 'authorization_code', }
        response = requests.post(token_endpoint, data=params)
        response_data = response.json()
        access_token = response_data.get('access_token')
        if not access_token:
            return 'Error: Failed to retrieve access token'

        # Store the access token in the session for future use
        session['access_token'] = access_token

        # Use the access token to retrieve the user's email address
        userinfo_endpoint = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_response = requests.get(userinfo_endpoint, headers=headers)
        userinfo = userinfo_response.json()
        email = userinfo.get('email')


        if email is None:
            abort(403)

        user = Worker.query.filter_by(email=email).first()
        if user is None:
            user = Boss.query.filter_by(email=email).first()
            if user is None:
                return redirect(url_for('auth.sign_up'))
            else:
                login_user(user)
                session.pop('access_token', None)
                return redirect(url_for('views.home'))
        else:
            login_user(user)
            session.pop('access_token', None)
            return redirect(url_for('views.home'))


    return redirect(url_for('auth.login'))


@externalcallback.route('/googlesignup', methods=['GET', 'POST'])
def googlesignup():
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if request.method == 'POST':
        if request.form.get('emailtogive') is not None and request.form.get('emailtogive') != '' and request.form.get(
                'nametogive') != '' and request.form.get('nametogive') is not None:
            email = request.form.get('emailtogive')
            name = request.form.get('nametogive')
            accounttype = request.form.get('accounttype')
            password = request.form.get('passwordtogive')

            if accounttype == 'worker':
                key = uuid.uuid4().hex[:12]
                new_user = Worker(email=email, first_name=name,
                                  password=generate_password_hash(password, method='sha256'), accounttype="worker",
                                  registrationid=key)
            elif accounttype == 'boss':
                new_user = Boss(email=email, first_name=name,
                                password=generate_password_hash(password, method='sha256'), accounttype="boss")
            else:
                flash("Error. Type not selected.", category='error')
                return redirect(url_for('auth.sign_up'))

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(getword("accountcreated", cookie), category='success')
            if accounttype == 'worker':
                sendregisterationemail(email, name, current_user.registrationid)
                return redirect(url_for('views.boss'))
            else:
                sendregisterationemailboss(email, name)
                return redirect(url_for('views.home'))

        else:
            csrf_token_cookie = request.cookies.get('g_csrf_token')
            if not csrf_token_cookie:
                abort(403)
            csrf_token_body = request.form.get('g_csrf_token')
            if not csrf_token_body:
                abort(403)
            if csrf_token_cookie != csrf_token_body:
                abort(403)

    for data in request.form:
        print(data)

    credentials = request.form.get('credential')
    if not credentials:
        abort(403)

    response = requests.get(check_url + credentials)
    if response.status_code != 200:
        abort(403)

    data = response.json()
    if data['aud'] != app.config['GOOGLE_CLIENT_ID']:
        abort(403)

    email = data['email']
    if not email:
        abort(403)

    email_verified = data['email_verified']
    if not email_verified:
        abort(403)

    exp = data['exp']
    if not exp:
        abort(403)

    # check if exp is in the past
    if float(exp) < time.time():
        abort(403)

    iss = data['iss']
    if not iss:
        abort(403)

    if iss != "accounts.google.com" and iss != "https://accounts.google.com":
        abort(403)

    sub = data['sub']
    if not sub:
        abort(403)

    name = data['name']
    if not name:
        abort(403)

    # check email is not already in use
    user = Worker.query.filter_by(email=email).first()
    if user:
        flash(getword("emailalreadyexists", cookie), category='error')
        return redirect(url_for('auth.sign_up'))
    user = Boss.query.filter_by(email=email).first()
    if user:
        flash(getword("emailalreadyexists", cookie), category='error')
        return redirect(url_for('auth.sign_up'))

    return render_template("googlesignup.html", user=current_user, worker=getword("worker", cookie),
                           boss=getword("boss", cookie), emailrequest=email, namerequest=name,
                           enterpassword=getword("enterpassword", cookie))


@externalcallback.route('/github/login', methods=['GET', 'POST'])
def githublogin():

    return redirect(
        "https://github.com/login/oauth/authorize?client_id=bd6042273acba34c7a84&scope=user:email,read:user&redirect_uri=https://tasklify.me/github/callback&")


@externalcallback.route('/github/callback', methods=['GET', 'POST'])
def githubcallback():
    cookie = request.cookies.get('locale')
    code = request.args.get('code')
    if code is None:
        print("No code")
        flash("Error. ", category='error')
        return redirect(url_for('auth.login'))

    load_dotenv()

    access_url = "https://github.com/login/oauth/access_token"

    data = {'client_id': 'bd6042273acba34c7a84',  # load from env file
            'client_secret': os.getenv('GITHUB_SECRET'), 'code': code}

    response = requests.post(access_url, data=data, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        print(response.json())
        flash("Error. ", category='error')
        return redirect(url_for('auth.login'))
    print(response.json())

    access_token = response.json()['access_token']

    user_url = "https://api.github.com/user"

    # post request to get user data with access token as BEARER OAuth token
    response = requests.get(user_url, headers={'Authorization': 'token ' + access_token})
    if response.status_code != 200:
        flash("Error. ", category='error')
        return redirect(url_for('auth.login'))

    data = response.json()
    email = data['email']
    name = data['name']

    # check if email is not already in use
    user = Worker.query.filter_by(email=email).first()
    if user:
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
    else:
        user = Boss.query.filter_by(email=email).first()
        if user:
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("githubsignup.html", user=current_user, worker=getword("worker", cookie),
                           boss=getword("boss", cookie), emailrequest=email, namerequest=name,
                           enterpassword=getword("enterpassword", cookie))


@externalcallback.route('/github/authorize', methods=['GET', 'POST'])
def githubauthorize():
    email = request.form.get('emailtogive')
    name = request.form.get('nametogive')
    accounttype = request.form.get('accounttype')
    password = request.form.get('passwordtogive')
    cookie = request.cookies.get('locale')

    if request.method == 'POST':
        if accounttype == 'worker':
            key = uuid.uuid4().hex[:12]
            new_user = Worker(email=email, first_name=name, password=generate_password_hash(password, method='sha256'),
                              accounttype="worker", registrationid=key)
        elif accounttype == 'boss':
            new_user = Boss(email=email, first_name=name, password=generate_password_hash(password, method='sha256'),
                            accounttype="boss")
        else:
            flash("Error. Type not selected.", category='error')
            return redirect(url_for('auth.sign_up'))

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash(getword("accountcreated", cookie), category='success')
        if accounttype == 'worker':
            sendregisterationemail(email, name, current_user.registrationid)
            return redirect(url_for('views.boss'))
        else:
            sendregisterationemailboss(email, name)
            return redirect(url_for('views.home'))


@externalcallback.route('/facebook/login', methods=['GET', 'POST'])
def facebooklogin():
    return redirect(
        "https://www.facebook.com/v16.0/dialog/oauth?client_id=697359442012060&redirect_uri=https://tasklify.me/facebook/callback&scope=email,public_profile&response_type=code&auth_type=rerequest&state=tskfl")


@externalcallback.route('/facebook/callback', methods=['GET', 'POST'])
def facebookcallback():

    # get the data from the request
    code = request.args.get('code')
    load_dotenv()
    if code is None:
        print("No code")
        flash("Error. ", category='error')
        return redirect(url_for('auth.login'))

    # get the access token
    access_url = "https://graph.facebook.com/v16.0/oauth/access_token"

    client_id = '697359442012060'
    client_secret = os.getenv('FACEBOOK_SECRET')
    redirect_uri = 'https://tasklify.me/facebook/callback'
    url = f"{access_url}?client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}"
    finalurl = url.replace(" ", "")
    response = requests.get(finalurl)

    if response.status_code != 200:
        print(response.json())
        flash("Error. ", category='error')
        return redirect(url_for('auth.login'))

    access_token = response.json()['access_token']
    inspect_url = "https://graph.facebook.com/debug_token"
    data = {'input_token': access_token, 'access_token': access_token}
    response = requests.get(inspect_url, params=data)
    if response.status_code != 200:
        print(response.json())
        flash("Error. ", category='error')
        return redirect(url_for('auth.login'))

    # get the user data
    user_url = "https://graph.facebook.com/v16.0/me"

    data = {'fields': 'id,name,email', 'access_token': access_token}
    response = requests.get(user_url, params=data)
    if response.status_code != 200:
        print(response.json())
        flash("Error. ", category='error')
        return redirect(url_for('auth.login'))

    data = response.json()
    email = data['email']
    name = data['name']

    # check if email is not already in use
    user = Worker.query.filter_by(email=email).first()
    if user:
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
    else:
        user = Boss.query.filter_by(email=email).first()
        if user:
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

    cookie = request.cookies.get('locale')

    # download the profile picture
    profile_url = "https://graph.facebook.com/v16.0/me/picture"
    data = {'redirect': 'false', 'access_token': access_token}
    response = requests.get(profile_url, params=data)
    if response.status_code != 200:
        print(response.json())
        flash("Error. ", category='error')
        return redirect(url_for('auth.login'))

    data = response.json()
    profilepic = data['data']['url']
    response = requests.get(profilepic)
    if response.status_code != 200:
        print(response.json())
        flash("Error. ", category='error')
        return redirect(url_for('auth.login'))

    emailwithnoat = email.replace("@", "")

    with open(f"static/pfp/TEMP-{emailwithnoat}.png", "wb") as f:
        f.write(response.content)


    return render_template("facebooksignup.html", user=current_user, worker=getword("worker", cookie),
                           boss=getword("boss", cookie), emailrequest=email, namerequest=name,
                           enterpassword=getword("enterpassword", cookie))


@externalcallback.route('/facebook/authorize', methods=['GET', 'POST'])
def facebookauthorize():
    email = request.form.get('emailtogive')
    name = request.form.get('nametogive')
    accounttype = request.form.get('accounttype')
    password = request.form.get('passwordtogive')
    cookie = request.cookies.get('locale')

    emailwithnoat = email.replace("@", "")


    if request.method == 'POST':
        if accounttype == 'worker':
            key = uuid.uuid4().hex[:12]
            new_user = Worker(email=email, first_name=name, password=generate_password_hash(password, method='sha256'),
                              accounttype="worker", registrationid=key)
        elif accounttype == 'boss':
            new_user = Boss(email=email, first_name=name, password=generate_password_hash(password, method='sha256'),
                            accounttype="boss")
        else:
            flash("Error. Type not selected.", category='error')
            return redirect(url_for('auth.sign_up'))

        db.session.add(new_user)
        db.session.commit()
        pfp = f"static/pfp/TEMP-{emailwithnoat}.png"
        os.rename(pfp, f"static/pfp/{new_user.id}.png")
        login_user(new_user, remember=True)
        flash(getword("accountcreated", cookie), category='success')
        if accounttype == 'worker':
            sendregisterationemail(email, name, current_user.registrationid)
            return redirect(url_for('views.boss'))
        else:
            sendregisterationemailboss(email, name)
            return redirect(url_for('views.home'))
