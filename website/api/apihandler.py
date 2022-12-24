import datetime
import os
import time
import uuid
from os.path import join, dirname, realpath

import pandas as pd
import requests
from dateutil import parser
from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import abort
from flask import jsonify
import json
from flask import current_app as app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename, send_from_directory

from website import CAPTCHA1
from .. import db
from ..mailsender import sendregisterationemail
from ..models import Task
from ..models import Worker, Boss
from ..translator import getword
from ..addtabs import addtabs
from ..fileshandler import fileshandler
import pandas

from ..translator import getword

api = Blueprint('api', __name__)

homepage = "views.home"
workerspage = "views.workers"
oneworkerpage = "views.worker"

global csrfg


@api.route('/api/v1/<token>/<worker>', methods=['GET'])
def getworker(token, worker):
    user = Worker.query.filter_by(token=token).first()
    worker = Worker.query.filter_by(id=worker).first()
    if user is None:
        user = Boss.query.filter_by(token=token).first()
        if user is None:
            return "Authorization invalid", 403

    if user.token != token:
        return "Authorization invalid", 403

    if user.accounttype == "worker":
        if worker.id != user.id:
            return "Your token does not allow you access different workers than yourself", 403
    elif user.accounttype == "boss":
        if worker not in user.workers:
            return "You are not allowed to access this worker", 403

    if worker is None:
        return "Worker does not exist", 404



    return worker.as_dict(), 200