import json
import os
from os.path import join, dirname, realpath

import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import current_app as app
from flask_login import login_required, current_user
from markupsafe import Markup
from werkzeug.utils import secure_filename, send_from_directory

from . import db
from .models import Worker, Boss
from .translator import getword, gettheme

fileshandler = Blueprint('fileshandler', __name__)

homepage = "views.home"
workerspage = "views.workers"
oneworkerpage = "views.worker"

global csrfg

# no potential security issue
allowed_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt',
                      'ods', 'odp', 'odg', 'odf', 'rtf', 'csv', 'zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'mp3', 'mp4',
                      'wav', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'mpg', 'mpeg', 'm4v', 'webm', 'vob', 'ogg', 'ogv',
                      '3gp', '3g2', 'm4a', 'flac', 'aac', 'wma', 'iso', 'apk', 'exe', 'jar', 'bat', 'cmd', 'vb', 'vbs',
                      'js', 'php', 'py', 'pl', 'rb', 'sh', 'html', 'htm', 'xhtml', 'asp', 'aspx', 'css', 'scss', 'sass',
                      'less', 'c', 'cpp', 'h', 'hpp', 'cs', 'java', 'class', 'jar', 'vb', 'vbs', 'js', 'php', 'py',
                      'pl', 'rb', 'sh', 'html', 'htm', 'xhtml', 'asp', 'aspx', 'css', 'scss', 'sass', 'less', 'c',
                      'cpp', 'h', 'hpp', 'cs', 'java', 'class', 'jar', 'vb', 'vbs', 'js', 'php', 'py', 'pl', 'rb', 'sh',
                      'html', 'htm', 'xhtml', 'asp', 'aspx', 'css', 'scss', 'sass', 'less', 'c', 'cpp', 'h', 'hpp',
                      'cs', 'java', 'class', 'jar', 'vb', 'vbs', 'js', 'php', 'py', 'pl', 'rb', 'sh', 'html', 'htm',
                      'xhtml', 'asp', 'aspx', 'css', 'scss', 'sass', 'less', 'c', 'cpp', 'h', 'hpp', 'cs', 'java',
                      'class', 'jar', 'vb', 'vbs', 'js', 'php', 'py', 'pl', 'rb', 'sh', 'html', 'htm', 'xhtml', 'asp',
                      'aspx', 'css', 'scss']


def allowed_file(filename):
    if len(filename.rsplit('.', 1)) > 2:
        return False
    else:
        extension = filename.rsplit('.', 1)[1].lower()
        if extension in allowed_extensions:
            return True


@fileshandler.route('/file/upld', methods=['GET', 'POST'])
@login_required
def fileupd():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # 100 mb
            if file.content_length > 100000000:
                flash("File is too big! Max size is 100 MB")
                return redirect(request.url)

            from transliterate import translit
            filenametranslit = file.filename
            if not all(ord(c) < 128 for c in file.filename):
                filenametranslit = translit(file.filename, reversed=True)

            # change all _ to -
            filenametranslit = filenametranslit.replace("_", "-")

            filename = secure_filename(filenametranslit)
            filename = filename.replace("_", "-")
            print(filename)
            finalfilename = str(current_user.id) + "_" + filename
            UPLOADS_PATH = join(dirname(realpath(__file__)), 'ugc/uploads/')
            path = join(UPLOADS_PATH, finalfilename)
            file.save(path)
    return redirect(f"/files/{current_user.id}")


@fileshandler.route('/uploaded_file/<filename>')
def uploaded_file(filename):

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if not current_user.is_authenticated:
        flash(getword("youneedtobeloggedin", cookie), category="error")
        return redirect(url_for('auth.login'))

    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        if current_user.accounttype == "worker":
            imageid = filename.split("_")[0]

            # check if imageid is either workerid or bossid
            worker = Worker.query.filter_by(id=imageid).first()
            if worker is None:
                boss = Boss.query.filter_by(id=imageid).first()
                if boss is None:
                    return redirect(url_for(homepage))
                else:
                    if current_user.boss_id != boss.id:
                        return redirect(url_for(homepage))
            else:
                if worker.id != current_user.id:
                    return redirect(url_for(homepage))
                # if file is previewable image or video or audio then return it else download it
                if filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav', 'avi',
                                                          'mov', 'mkv', 'flv', 'wmv', 'mpg', 'mpeg', 'm4v', 'webm',
                                                          'vob', 'ogg', 'ogv', '3gp', '3g2', 'm4a', 'flac', 'aac',
                                                          'wma', 'pdf', 'txt']:
                    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)
                else:
                    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True,
                                               environ=request.environ)


        elif current_user.accounttype == "boss":
            imageid = filename.split("_")[0]
            if Boss.query.filter_by(id=imageid).first() is not None:
                if Boss.query.filter_by(id=imageid).first().id == current_user.id:
                    if filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav', 'avi',
                                                              'mov', 'mkv', 'flv', 'wmv', 'mpg', 'mpeg', 'm4v', 'webm',
                                                              'vob', 'ogg', 'ogv', '3gp', '3g2', 'm4a', 'flac', 'aac',
                                                              'wma', 'pdf', 'txt']:
                        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)
                    else:
                        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True,
                                                   environ=request.environ)
            elif Worker.query.filter_by(id=imageid).first() is not None:
                if Worker.query.filter_by(id=imageid).first().boss_id == current_user.id:
                    if filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav', 'avi',
                                                              'mov', 'mkv', 'flv', 'wmv', 'mpg', 'mpeg', 'm4v', 'webm',
                                                              'vob', 'ogg', 'ogv', '3gp', '3g2', 'm4a', 'flac', 'aac',
                                                              'wma', 'pdf', 'txt']:
                        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)
                    else:
                        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True,
                                                   environ=request.environ)

            flash(getword("nopermtoviewthisview", cookie), category="error")
            return redirect(url_for(homepage))

    index = len(filename.rsplit('.', 1))

    if filename.rsplit('.', 1)[index].lower() in ['png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav', 'avi', 'mov', 'mkv',
                                                  'flv', 'wmv', 'mpg', 'mpeg', 'm4v', 'webm', 'vob', 'ogg', 'ogv',
                                                  '3gp', '3g2', 'm4a', 'flac', 'aac', 'wma', 'pdf', 'txt']:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, environ=request.environ)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True, environ=request.environ)


@fileshandler.route("/ugc/uploads/<filename>", methods=["GET"])
def get_file(filename):
    return redirect(url_for('fileshandler.uploaded_file', filename=filename))


def hastebin(text):
    r = requests.post("https://hastebin.com/documents", data=text)
    return "https://hastebin.com/raw/" + r.json()["key"]


@fileshandler.route("/files/<path:id>", methods=["GET", "POST"])
def files(id):
    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
    else:
        cookie = 'en'

    if current_user.accounttype == "worker":
        if current_user.id != id:
            flash(getword("workernotfound", cookie), category="error")
            return redirect(url_for(homepage))
    elif current_user.accounttype == "boss":
        if current_user.id != id:
            if Worker.query.filter_by(id=id).first().boss_id != current_user.id:
                flash(getword("workernotfound", cookie), category="error")
                return redirect(url_for(homepage))

    # check static/uploads for files starting with id
    files = {}
    splitnames = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        # split by _
        file1 = file.split("_")
        if str(file1[0]) == str(id):
            files[file] = file1[1]

    for file in str(current_user.googlefiles).split("|GOOGLEDOCSFILESEPARATOR|"):
        print(file)
        if file.rstrip() != "" and file is not None and file != "None":
            newfile = "GOOGLEDOC||" + file
            files[newfile] = file

    print(files)







    if request.method == "POST":
        if request.form.get("typeform") == "delete":
            file = request.form.get("file")
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
            except Exception as e:
                print(e)
                flash(getword("error", cookie), category="error")
                return redirect(url_for("fileshandler.files", id=id))
            return redirect(url_for("fileshandler.files", id=id))
        elif request.form.get("typeform") == "googledocscreate":
            if current_user.googleauthed == "1" and current_user.google_access_token is not None and current_user.google_refresh_token is not None:

                url = 'https://docs.googleapis.com/v1/documents'
                document_content = {'title': 'My new document'}

                headers = {'Authorization': f'Bearer {current_user.google_access_token}',
                           'Content-Type': 'application/json'}

                response = requests.post(url, headers=headers, data=json.dumps(document_content))

                if response.status_code == 200:
                    document_id = response.json()['documentId']
                    print(f'Successfully created new document with ID: {document_id}')
                    message = Markup(
                        "Google Docs document created. <a href='https://docs.google.com/document/d/" + document_id + "/edit' target='_blank'>Click here to edit</a>")
                    flash(message, category="success")
                    googlefiles = current_user.googlefiles
                    if googlefiles is None:
                        googlefiles = ""

                    googlefilesnew = googlefiles + document_id + "|GOOGLEDOCSFILESEPARATOR|"
                    current_user.googlefiles = googlefilesnew
                    db.session.commit()
                    return redirect(url_for("fileshandler.files", id=id))
                else:
                    print('Failed to create new document')
                    flash("Failed to create new document", category="error")
                    return redirect(url_for("fileshandler.files", id=id))

    return render_template("files.html", calendar=getword("calendar", cookie), profilenav=getword("profilenav", cookie),
                           loginnav=getword("loginnav", cookie), signupnav=getword("signupnav", cookie),
                           tasksnav=getword("tasksnav", cookie), workersnav=getword("workersnav", cookie),
                           adminnav=getword("adminnav", cookie), logoutnav=getword("logoutnav", cookie),
                           homenav=getword("homenav", cookie), user=current_user, files=files, splitnames=splitnames,
                           delete=getword("delete", cookie), chatnav=getword("chatnav", cookie),
                           uploadtext=getword("uploadtext", cookie), myfiles=getword("myfiles", cookie),
                           fileuploadtext=getword("fileuploadtext", cookie), theme=gettheme(request),
                           creategoogledoc=getword("creategoogledoc", cookie), creategoogleslides=getword("creategoogleslides", cookie),
                           creategooglespreadsheets=getword("creategooglespreadsheets", cookie))
