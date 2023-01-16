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

        messagelist.append({"id": message.idmessage, "sender": is_sender(), "date": datetostring(message.date),
                            "message": message.message})

    messagelist.sort(key=lambda x: x["date"])

    return messagelist, 200


@chathandler.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    id = current_user.id

    if 'locale' in request.cookies:
        cookie =  request.cookies.get('locale')
    else:
        cookie = 'en'

    if request.method == 'POST':
        if request.form.get('typeform') == 'message':
            if request.form.get('message') is not None:
                message = request.form.get('message')
                id_receiver = request.form.get('id_receiver')
                chatid = request.form.get('chat_id')
                if message != "":
                    import datetime
                    # noinspection PyArgumentList
                    newmessage = Message(chat=chatid, id_sender=current_user.id, id_receiver=id_receiver,
                                         message=message, date=datetime.datetime.now())
                    db.session.add(newmessage)
                    db.session.commit()
        elif request.form.get('typeform') == 'delete':
            idmessage = request.form.get('idmessage')
            message = Message.query.get(idmessage)
            userid = request.form.get('userid')
            if userid != current_user.id:
                return "You are not allowed to access this page", 403
            if message is not None:
                db.session.delete(message)
                db.session.commit()

    chats = []

    for chat in Chat.query.filter_by(id_creator=id).all():
        is_creator = False
        if chat.id_creator == id:
            is_creator = True
        chats.append({"id": chat.id, "id_participant": chat.id_participant, "id_creator": chat.id_creator,
                      "name_creator": chat.name_creator, "name_participant": chat.name_participant,
                      'image_participant': '/static/pfp/' + chat.id_participant + '.png',
                      'image_creator': '/static/pfp/' + chat.id_creator + '.png', 'is_creator': is_creator})
    for chat in Chat.query.filter_by(id_participant=id).all():
        is_creator = False
        if chat.id_creator == id:
            is_creator = True
        chats.append({"id": chat.id, "id_participant": chat.id_participant, "id_creator": chat.id_creator,
                      "name_creator": chat.name_creator, "name_participant": chat.name_participant,
                      'image_participant': '/static/pfp/' + chat.id_participant + '.png',
                      'image_creator': '/static/pfp/' + chat.id_creator + '.png', 'is_creator': is_creator})


    print(chats)

    basepath = None
    print(request.host)
    if request.host == '127.0.0.1:5000':
        basepath = 'http://127.0.0.1:5000'
    else:
        basepath = 'https://www.tasklify.me'


    return render_template('chat.html', user=current_user, userid=id, chats=chats,
                           profilenav=getword("profilenav", cookie), loginnav=getword("loginnav", cookie),
                           signupnav=getword("signupnav", cookie), tasksnav=getword("tasksnav", cookie),
                           workersnav=getword("workersnav", cookie), adminnav=getword("adminnav", cookie),
                           logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie), chatnav=getword("chatnav", cookie),
                           basepath=basepath)


@chathandler.route('/chatapi/<id>/<otherid>', methods=['GET'])
@login_required
def chatapi(id, otherid):

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

    user1 = Worker.query.filter_by(id=id).first()
    user2 = Worker.query.filter_by(id=otherid).first()

    if user1 is None:
        user1 = Boss.query.filter_by(id=id).first()
    if user2 is None:
        user2 = Boss.query.filter_by(id=otherid).first()

    if user1 is None or user2 is None:
        return "User not found", 404

    return render_template('chatapi.html', user=current_user, userid=id, otherid=otherid, chat=chat, chatid=chat.id,
                           user1=user1, user2=user2)
