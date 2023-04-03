import time
import uuid
from os.path import join, dirname, realpath

import transliterate
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

        messagelist.append(
            {"id": message.idmessage, "sender": is_sender(), "date": message.date, "message": message.message})

    # sort messages by date, make sure the newest message is at the bottom and that month is also sorted
    messagelist = sorted(messagelist, key=lambda k: k['date'])

    for message in messagelist:
        message['date'] = datetostring(message['date'])

    return messagelist, 200


@chathandler.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    id = current_user.id

    if 'locale' in request.cookies:
        cookie = request.cookies.get('locale')
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
                    # make date in utc+2
                    newmessage = Message(chat=chatid, id_sender=current_user.id, id_receiver=id_receiver,
                                         message=message, date=datetime.datetime.now() + datetime.timedelta(hours=2))
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
        elif request.form.get('typeform') == 'createchat':
            useridtoadd = request.form.get('chatpartnerid')
            if useridtoadd == current_user.id:
                return redirect(url_for('chathandler.chat'))
            if Worker.query.get(useridtoadd) is None and Boss.query.get(useridtoadd) is None:
                return redirect(url_for('chathandler.chat'))

            chat = Chat.query.filter_by(id_creator=current_user.id, id_participant=useridtoadd).first()
            if chat is None:
                chat = Chat.query.filter_by(id_creator=useridtoadd, id_participant=current_user.id).first()
                if chat is None:
                    if Worker.query.get(useridtoadd) is not None:
                        current_user_name = current_user.first_name
                        if not current_user_name.isascii():
                            current_user_name= transliterate.translit(current_user_name, reversed=True)
                        current_user_name = current_user_name.rstrip()

                        usertoadd_name = Worker.query.get(useridtoadd).first_name
                        if not usertoadd_name.isascii():
                            usertoadd_name= transliterate.translit(usertoadd_name, reversed=True)
                        usertoadd_name = usertoadd_name.rstrip()

                        newchat = Chat(id_creator=current_user.id, id_participant=useridtoadd,
                                       name_creator=current_user_name,
                                       name_participant=usertoadd_name)
                    else:
                        current_user_name = current_user.first_name
                        if not current_user_name.isascii():
                            current_user_name = transliterate.translit(current_user_name, reversed=True)
                        current_user_name = current_user_name.rstrip()

                        usertoadd_name = Boss.query.get(useridtoadd).first_name
                        if not usertoadd_name.isascii():
                            usertoadd_name = transliterate.translit(usertoadd_name, reversed=True)
                        usertoadd_name = usertoadd_name.rstrip()

                        newchat = Chat(id_creator=current_user.id, id_participant=useridtoadd,
                                       name_creator=current_user_name, name_participant=usertoadd_name)

                    db.session.add(newchat)
                    db.session.commit()
                    return redirect(url_for('chathandler.chat'))
                else:
                    return redirect(url_for('chathandler.chat'))

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
                           logoutnav=getword("logoutnav", cookie), homenav=getword("homenav", cookie),
                           chatnav=getword("chatnav", cookie), basepath=basepath,
                           enteridofchatpartner=getword("enteridofchatpartner", cookie),
                           idislocatedinprofilepage=getword("idislocatedinprofilepage", cookie),
                           idisnotvalid=getword("idisnotvalid", cookie), chatcreated=getword("chatcreated", cookie),
                           otherpersoncanclosethechatatanytime=getword("otherpersoncanclosethechatatanytime", cookie),
                           createchat=getword("createchat", cookie), chatpartner=getword("chatpartner", cookie),
                           chatpartnerid=getword("chatpartnerid", cookie))


@chathandler.route('/chatapi/<id>/<otherid>', methods=['GET'])
@login_required
def chatapi(id, otherid):
    print("1")

    if not current_user.is_authenticated:
        return "not authenticated", 401

    print("2")

    if id != current_user.id:
        return "You are not allowed to access this page", 403

    print("3")

    # check if id exists
    if Worker.query.get(id) is None and Boss.query.get(id) is None:
        return "User not found", 404

    print("4")

    # check if otherid exists
    if Worker.query.get(otherid) is None and Boss.query.get(otherid) is None:
        return "User not found", 404

    print("5")

    # check if chat exists
    chat = Chat.query.filter_by(id_creator=id, id_participant=otherid).first()
    if chat is None:
        chat = Chat.query.filter_by(id_creator=otherid, id_participant=id).first()
        if chat is None:
            return "Chat not found", 404

    print("6")

    user1 = Worker.query.filter_by(id=id).first()
    user2 = Worker.query.filter_by(id=otherid).first()

    print("7")

    if user1 is None:
        user1 = Boss.query.filter_by(id=id).first()
    if user2 is None:
        user2 = Boss.query.filter_by(id=otherid).first()

    print("8")

    if user1 is None or user2 is None:
        return "User not found", 404

    print("9")

    return render_template('chatapi.html', user=current_user, userid=id, otherid=otherid, chat=chat, chatid=chat.id,
                           user1=user1, user2=user2)


@chathandler.route("/chat/block/<id>", methods=['GET', 'POST'])
@login_required
def block(id):

    if not current_user.is_authenticated:
        abort(403)

    if id == current_user.id:
        return redirect(url_for('chathandler.chat'))

    if Worker.query.get(id) is None and Boss.query.get(id) is None:
        return redirect(url_for('chathandler.chat'))

    if Worker.query.get(current_user.id) is None and Boss.query.get(current_user.id) is None:
        return redirect(url_for('chathandler.chat'))

    if Worker.query.get(id) is not None:
        otheruser = Worker.query.get(id)
    else:
        otheruser = Boss.query.get(id)

    if otheruser is None:
        return redirect(url_for('chathandler.chat'))

    if current_user.accounttype == "worker":
        if current_user.boss_id == otheruser.id:
            flash("You can't block your employer", category="error")
            return redirect(url_for('chathandler.chat'))

    if current_user.accounttype == "boss":
        if otheruser.boss_id == current_user.id:
            flash("You can't block your employee", category="error")
            return redirect(url_for('chathandler.chat'))

    chat = Chat.query.filter_by(id_creator=current_user.id, id_participant=otheruser.id).first()
    if chat is None:
        chat = Chat.query.filter_by(id_creator=otheruser.id, id_participant=current_user.id).first()
        if chat is None:
            return redirect(url_for('chathandler.chat'))

    db.session.delete(chat)
    db.session.commit()

    flash("Chat blocked", category="success")
    return redirect(url_for('chathandler.chat'))
