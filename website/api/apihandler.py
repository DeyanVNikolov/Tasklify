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


@api.app_errorhandler(404)
def page_not_found(e):
    return "404", 404


@api.route('/v1/employee/<token>/<worker>', methods=['GET', 'POST'])
def worker(token, worker):

    print("token: " + token)
    print("worker: " + worker)

    if request.method == 'POST':
        return jsonify({"status": "error", "message": "POST method is not allowed for this operation. See documentation for more information."}), 405


    if token == "not_defined_variable" or worker == "not_defined_variable":
        return jsonify({"error": "Missing required parameters"}), 400


    user_from_token = Worker.query.filter_by(token=token).first()
    if not user_from_token:
        user_from_token = Boss.query.filter_by(token=token).first()
    if not user_from_token:
        return jsonify({"error": "Authentication failed"}), 403

    worker = Worker.query.filter_by(id=worker).first()
    if not worker:
        return jsonify({"error": "Worker not found"}), 404


    if user_from_token.accounttype == "worker":
        if worker.id != user_from_token.id:
            return jsonify({"error": "Your current token is not allowed to access this worker"}), 403
    else:
        if worker.boss_id != user_from_token.id:
            return jsonify({"error": "Your current token is not allowed to access this worker"}), 403


    workerdict = worker.to_dict()

    return jsonify({"status": "success", "worker": workerdict}), 200

@api.route('/v1/employee/<token>/<worker>/tasks', methods=['GET', 'POST'])
def worker_tasks(token, worker):

        print("token: " + token)
        print("worker: " + worker)

        if request.method == 'POST':
            return jsonify({"status": "error", "message": "POST method is not allowed for this operation. See documentation for more information."}), 405


        if token == "not_defined_variable" or worker == "not_defined_variable":
            return jsonify({"error": "Missing required parameters"}), 400


        user_from_token = Worker.query.filter_by(token=token).first()
        if not user_from_token:
            user_from_token = Boss.query.filter_by(token=token).first()
            if not user_from_token:
                return jsonify({"error": "Authentication failed"}), 403

        worker = Worker.query.filter_by(id=worker).first()
        if not worker:
            return jsonify({"error": "Worker not found"}), 404


        if user_from_token.accounttype == "worker":
            if worker.id != user_from_token.id:
                return jsonify({"error": "Your current token is not allowed to access this worker"}), 403

        else:
            if worker.boss_id != user_from_token.id:
                return jsonify({"error": "Your current token is not allowed to access this worker"}), 403

        tasks = Task.query.filter_by(worker_id=worker.id).all()
        tasksdict = {}
        for task in tasks:
            tasksdict[str(task.id)] = task.to_dict()

        return jsonify({"status": "success", "tasks": tasksdict}), 200


@api.route('/v1/employee/<token>/<worker>/tasks/<task>', methods=['GET', 'POST'])
def worker_task(token, worker, task):

        print("token: " + token)
        print("worker: " + worker)
        print("task: " + task)

        if request.method == 'POST':
            return jsonify({"status": "error", "message": "POST method is not allowed for this operation. See documentation for more information."}), 405


        if token == "not_defined_variable" or worker == "not_defined_variable" or task == "not_defined_variable":
            return jsonify({"error": "Missing required parameters"}), 400


        user_from_token = Worker.query.filter_by(token=token).first()
        if not user_from_token:
            user_from_token = Boss.query.filter_by(token=token).first()
            if not user_from_token:
                return jsonify({"error": "Authentication failed"}), 403

        worker = Worker.query.filter_by(id=worker).first()
        if not worker:
            return jsonify({"error": "Worker not found"}), 404


        if user_from_token.accounttype == "worker":
            if worker.id != user_from_token.id:
                return jsonify({"error": "Your current token is not allowed to access this worker"}), 403

        else:
            if worker.boss_id != user_from_token.id:
                return jsonify({"error": "Your current token is not allowed to access this worker"}), 403

        task = Task.query.filter_by(id=task).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        if task.worker_id != worker.id:
            return jsonify({"error": "Your current token is not allowed to access this task"}), 403

        taskdict = task.to_dict()

        return jsonify({"status": "success", "task": taskdict}), 200


