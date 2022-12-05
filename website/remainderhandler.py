from .models import Worker, Boss
from .models import Task
from .translator import getword

from .mailsender import sendremainder

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, send_from_directory, jsonify
from flask import current_app as app
from flask_login import login_required, current_user


for worker in Worker.query.all():
    uncompletedtasks = Task.query.filter_by(worker_id=worker.id, complete=0).all()
    uncompletedtasks2 = Task.query.filter_by(worker_id=worker.id, complete=1).all()
    total = len(uncompletedtasks) + len(uncompletedtasks2)
    if total > 0:
        sendremainder(worker.email, worker.first_name, total)



