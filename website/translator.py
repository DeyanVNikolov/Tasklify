from flask import request, current_app
from flask_login import current_user, login_required
import time
words = {

    "email": {
        "en": "Email Address",
        "bg": "Електронна поща",
    },
    "emailshort": {
        "en": "Email",
        "bg": "Ел. поща",
    },
    "password": {
        "en": "Password",
        "bg": "Парола",
    },
    "enteremail": {
        "en": "Enter Email",
        "bg": "Въведете имейл",
    },
    "login": {
        "en": "Login",
        "bg": "Вход",
    },
    "profiletext": {
        "en": "Profile",
        "bg": "Профил",
    },
    "name": {
        "en": "Name",
        "bg": "Име",
    },
    "changepassword": {
        "en": "Change Password",
        "bg": "Смяна на парола",
    },
    "deleteaccount": {
        "en": "Delete Account",
        "bg": "Изтриване на акаунт",
    },
    "oldpassword": {
        "en": "Old Password",
        "bg": "Стара парола",
    },
    "newpassword": {
        "en": "New Password",
        "bg": "Нова парола",
    },
    "cnewpassword": {
        "en": "Confirm Password",
        "bg": "Потвърдете паролата",
    },
    "confirm": {
        "en": "By checking this box and clicking the 'change password' button, you agree that you want to change your account password, making the old password invalid immediately after clicking the button.",
        "bg": "Отметнете тази кутийка и натиснете бутона 'Смяна на парола', за да потвърдите, че искате да смените паролата си, като старата парола става невалидна веднага след натискането на бутона.",
    },
    "enterpassword": {
        "en": "Enter Password",
        "bg": "Въведете парола",
    },
    "confirmdelete": {
        "en": "By checking this box and clicking the 'delete account' button, you agree that you want to delete your account, making it impossible to recover it.",
        "bg": "Отметнете тази кутийка и натиснете бутона 'Изтриване на акаунт', за да потвърдите, че искате да изтриете акаунта си, като той става невъзможен за възстановяване.",
    },
    "submit": {
        "en": "Submit",
        "bg": "Изпрати",
    },
    "firstandlast": {
        "en": "First and Last Name",
        "bg": "Име и фамилия",
    },
    "signup": {
        "en": "Sign Up",
        "bg": "Регистрация",
    },
    "alreadyhaveaccount": {
        "en": "Already have an account?",
        "bg": "Вече имате акаунт?",
    },
    "loginhere": {
        "en": "Login here",
        "bg": "Влезте тук",
    },
    "registerhere": {
        "en": "Register here",
        "bg": "Регистрирайте се тук",
    },
    "notregistered": {
        "en": "Not registered?",
        "bg": "Не сте регистрирани?",
    },
    "boss": {
        "en": "Boss",
        "bg": "Шеф",
    },
    "accessmessage": {
        "en": "In order to access any other page, your boss must register you first.",
        "bg": "За да имате достъп до други страници, шефът ви трябва да ви регистрира първо.",
    },
    "youridtext": {
        "en": "Your ID. Give it to your boss, so he can register you.",
        "bg": "Вашият ID. Дайте го на шефа си, за да ви регистрира.",
    },
    "delete": {
        "en": "Delete",
        "bg": "Изтрий",
    },
    "add": {
        "en": "Add",
        "bg": "Добави",
    },
    "tasktext": {
        "en": "Task",
        "bg": "Задача",
    },
    "statustext": {
        "en": "Status",
        "bg": "Статус",
    },
    "workertext": {
        "en": "Worker",
        "bg": "Работник",
    },
    "done": {
        "en": "Done",
        "bg": "Готово",
    },
    "tasktextplural": {
        "en": "Tasks",
        "bg": "Задачи",
    },
    "NotStarted": {
        "en": "Not Started",
        "bg": "Не е започната",
    },
    "completed": {
        "en": "Completed",
        "bg": "Завършена",
    },
    "addtask": {
        "en": "Add Task",
        "bg": "Добави задача",
    },
    "selectall": {
        "en": "Select All",
        "bg": "Избери всички",
    },
    "deselectall": {
        "en": "Deselect All",
        "bg": "Отмени избора",
    },
    "workermenu": {
        "en": "Worker Menu",
        "bg": "Меню на работника",
    },
    "moreinfo": {
        "en": "More Info",
        "bg": "Повече информация",
    },
    "tasktitle": {
        "en": "Task Title",
        "bg": "Заглавие на задачата",
    },
    "notdone": {
        "en": "Not Done",
        "bg": "Не е готово",
    },
    "selectworkers": {
        "en": "Select Workers",
        "bg": "Избери работници",
    },
    "idtext": {
        "en": "ID",
        "bg": "ID",
    },
    "addworker": {
        "en": "Add Worker",
        "bg": "Добави работник",
    },
    "youllberedirectedto": {
        "en": "You'll be redirected to",
        "bg": "Ще бъдете пренасочени към",
    },
    "infiveseconds": {
        "en": "in 5 seconds",
        "bg": "след 5 секунди",
    },
    "oryoucango": {
        "en": "or you can go to",
        "bg": "или можете да отидете на",
    },
    "here": {
        "en": "click here",
        "bg": "натиснете тук",
    },
    "home": {
        "en": "home",
        "bg": "начало",
    },
    "thirdpartylink": {
        "en": "Please note that this is a third party link and we are not responsible for its content.",
        "bg": "Моля, имайте предвид, че това е връзка на трета страна и не сме отговорни за нейното съдържание.",
    },
    "ifyourenotredirected": {
        "en": "If you are not redirected automatically,",
        "bg": "Ако не бъдете пренасочени автоматично,",
    },
    "contact": {
        "en": "Contact",
        "bg": "Контакт",
    },
    "contactus": {
        "en": "Contact Us",
        "bg": "Свържете се с нас",
    },
    "contactusmessage": {
        "en": "If you have any questions, please contact us.",
        "bg": "Ако имате въпроси, моля, свържете се с нас.",
    },
    "contactname": {
        "en": "Deyan Vladimirov Nikolov",
        "bg": "Деян Владимиров Николов",
    },
    "contactemail": {
        "en": "deyannikolov25@itpg-varna.bg",
        "bg": "deyannikolov25@itpg-varna.bg"
    },
    "databeingproccessed": {
        "en": "Your data is being processed. Please wait and do not refresh the page.",
        "bg": "Вашите данни се обработват. Моля, изчакайте и не актуализирайте страницата.",
    },
    "print": {
        "en": "Print",
        "bg": "Печат",
    },
    "workeridtext": {
        "en": "Worker ID",
        "bg": "ID на работника",
    },
    "workeremailtext": {
        "en": "Worker Email",
        "bg": "Имейл на работника",
    },
    "workernametext": {
        "en": "Worker Name",
        "bg": "Име на работника",
    },
    "taskstatustext": {
        "en": "Task Status",
        "bg": "Статус на задачата",
    },
    "requestedbytext": {
        "en": "Requested By",
        "bg": "Заявена от",
    },
    "attext": {
        "en": "at",
        "bg": "в",
    },
    "submitcodetext": {
        "en": "You can submit your code through here to get a shareable link.",
        "bg": "Можете да представите своя код чрез тук, за да получите връзка, която можете да споделите.",
    },
    "sevendaylimit": {
        "en": "Your code will be available at this link for 7 days. After that, it will be deleted automatically.",
        "bg": "Вашият код ще бъде наличен на тази връзка за 7 дни. След това ще бъде изтрит автоматично.",
    },
    "copy": {
        "en": "Copy",
        "bg": "Копирай",
    },
    "photouploader": {
        "en": "Photo Uploader",
        "bg": "Качване на снимка",
    },
    "markyourtaskasdonetext": {
        "en": "Add any photo link, code link or personal comments in the field and mark your task as done.",
        "bg": "Добавете връзка за снимка, връзка за код или лични коментари в полето и маркирайте задачата си като изпълнена.",
    },
    "photolinktexttitle": {
        "en": "Photo Link",
        "bg": "Връзка за снимка",
    },
    "idemail": {
        "en": "Your registration ID was sent to your email.",
        "bg": "Вашият регистрационен ID беше изпратен на вашия имейл.",
    },
    "starttext": {
        "en": "Start",
        "bg": "Старт",
    },
    "started": {
        "en": "Started",
        "bg": "Стартиран",
    },
    "deletefromall": {
        "en": "Delete this task from all workers",
        "bg": "Изтрий тази задача от всички",
    },




}



def getword(word, target):
    if word in words:
        if target in words[word]:
            return words[word][target]
        else:
            return "No translation for " + target
    else:
        return "!!! WORD NOT FOUND !!! " + word

def loadtime():
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)
    return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())


loadtime()


