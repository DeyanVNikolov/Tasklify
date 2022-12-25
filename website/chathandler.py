import time
import uuid
from os.path import join, dirname, realpath

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import db
from .models import Task
from .models import Worker
from .models import Boss
from .models import Message
from .models import Chat
from .translator import getword

chathandler = Blueprint('chathandler', __name__)

homepage = "views.home"
workerspage = "views.workers"
oneworkerpage = "views.worker"

global csrfg

@chathandler.route('/messageget/<id>/<otherid>', methods=['GET', 'POST'])
@login_required
def messageget(id, otherid):
    abort(403)
    id = current_user.id
    if not current_user.is_authenticated:
        return "not authenticated", 401

    if id != current_user.id:
        return "You are not allowed to access this page", 403

    # check if id exists
    if Worker.query.get(id) is None and Boss.query.get(id) is None:
        return "User not found", 404

    # check if otherid exists
    if Worker.query.get(otherid) is None and Boss.query.get(otherid) is None:
        return "User not found", 404

    # check if chat exists
    chat = Chat.query.filter_by(id_creator=id, id_participant=otherid).first()
    if chat is None:
        chat = Chat.query.filter_by(id_creator=otherid, id_participant=id).first()
        if chat is None:
            return "Chat not found", 404

    refresh = True

    # get all messages of chat
    messages = Message.query.filter_by(chat=chat.id).all()

    messagelist = []

    for message in messages:
        def is_sender():
            if message.id_sender == id:
                return True
            else:
                return False

        def datetostring(date):
            return date.strftime("%d.%m.%Y %H:%M:%S")

        messagelist.append({
            "id": message.idmessage,
            "sender": is_sender(),
            "date": datetostring(message.date),
            "message": message.message
        })

    messagelist.sort(key=lambda x: x["date"])

    return messagelist, 200

@chathandler.route('/chat', methods=['GET', 'POST'])
def chat():
    abort(403)
    id = current_user.id

    chats=[]

    for chat in Chat.query.filter_by(id_creator=id):
        chats.append(chat)
    for chat in Chat.query.filter_by(id_participant=id):
        chats.append(chat)


    return render_template('chat.html', user=current_user, userid=id, chats=chats)


@chathandler.route('/chat/<workerid>', methods=['GET', 'POST'])
@login_required
def chatwithworker(workerid):
    abort(403)
    chat = Chat.query.filter_by(id=workerid).first()

    if chat is None:
        abort(404)

    # check if both creator_id and participant_id are existing
    creator = Worker.query.filter_by(id=chat.id_creator).first()
    participant = Worker.query.filter_by(id=chat.id_participant).first()

    # if either of them is none try again with boss
    if creator is None:
        creator = Boss.query.filter_by(id=chat.id_creator).first()
    if participant is None:
        participant = Boss.query.filter_by(id=chat.id_participant).first()



    if creator is None or participant is None:
        abort(404)

    # check if current user is creator or participant
    if current_user.id != creator.id and current_user.id != participant.id:
        abort(404)

    if request.method == 'POST':
        if request.form.get('message') is not None:
            message = request.form.get('message')
            id_receiver = request.form.get('id_receiver')
            if message != "":
                newmessage = Message(chat=chat.id, id_sender=current_user.id, id_receiver=id_receiver, message=message)
                db.session.add(newmessage)
                db.session.commit()



    return render_template('chatwithworker.html', user=current_user, workerid=workerid, userid=current_user.id, otherid=creator.id if creator.id != current_user.id else participant.id, chat=chat)

@chathandler.route('/chatapi/<id>/<otherid>', methods=['GET'])
@login_required
def chatapi(id, otherid):
    abort(403)

    if not current_user.is_authenticated:
        return "not authenticated", 401

    if id != current_user.id:
        return "You are not allowed to access this page", 403

    # check if id exists
    if Worker.query.get(id) is None and Boss.query.get(id) is None:
        return "User not found", 404

    # check if otherid exists
    if Worker.query.get(otherid) is None and Boss.query.get(otherid) is None:
        return "User not found", 404

    # check if chat exists
    chat = Chat.query.filter_by(id_creator=id, id_participant=otherid).first()
    if chat is None:
        chat = Chat.query.filter_by(id_creator=otherid, id_participant=id).first()
        if chat is None:
            return "Chat not found", 404




    return render_template('chatapi.html', user=current_user, userid=id, otherid=otherid, chat=chat)
