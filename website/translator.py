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
        "bg": "Отмятайки тази кутийка и натискайки бутона 'Смяна на парола', за да потвърдите, че искате да смените паролата си, като старата парола става невалидна веднага след натискането на бутона.",
    },
    "enterpassword": {
        "en": "Enter Password",
        "bg": "Въведете парола",
    },
    "confirmdelete": {
        "en": "By checking this box and clicking the 'delete account' button, you agree that you want to delete your account, making it impossible to recover it.",
        "bg": "Отмятайки тази кутийка и натискайки бутона 'Изтриване на акаунт', за да потвърдите, че искате да изтриете акаунта си, като той става невъзможен за възстановяване.",
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
        "en": "Employee",
        "bg": "Служител",
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
        "en": "Employee Menu",
        "bg": "Меню на служител",
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
        "en": "Select Employees",
        "bg": "Избери служители",
    },
    "idtext": {
        "en": "ID",
        "bg": "ID",
    },
    "addworker": {
        "en": "Add Employee",
        "bg": "Добави служител",
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
        "en": "Click here",
        "bg": "Натиснете тук",
    },
    "myfiles": {
        "en": "My Files",
        "bg": "Моите файлове",
    },
    "empmyfiles": {
        "en": "Employee Files",
        "bg": "Файлове на служител",
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
        "en": "Employee ID",
        "bg": "ID на служител",
    },
    "workeremailtext": {
        "en": "Employee Email",
        "bg": "Имейл на служител",
    },
    "workernametext": {
        "en": "Employee Name",
        "bg": "Име на служител",
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
        "en": "Delete this task from all employees",
        "bg": "Изтрий тази задача от всички служители",
    },
    "missingid": {
        "en": "Missing ID",
        "bg": "Липсващ ID",
    },
    "noworkerwithid": {
        "en": "No employee with that ID",
        "bg": "Няма работник с този ID",
    },
    "workeradded": {
        "en": "Еmployee added",
        "bg": "Служител добавен",
    },
    "workeralreadyremoved": {
        "en": "Employee already removed",
        "bg": "Служителът вече е премахнат",
    },
    "workerremoved": {
        "en": "Employee removed",
        "bg": "Служител премахнат",
    },
    "workeralreadyadded": {
        "en": "Employee already added",
        "bg": "Служителът вече е добавен",
    },
    "missingtask": {
        "en": "Missing task",
        "bg": "Липсваща задача",
    },
    "noworkersselected": {
        "en": "No employees selected",
        "bg": "Няма избрани служители",
    },
    "taskadded": {
        "en": "Task added",
        "bg": "Задачата е добавена",
    },
    "youcantedittask": {
        "en": "You can't edit this task",
        "bg": "Не можете да редактирате тази задача",
    },
    "youneedtobeloggedin": {
        "en": "You need to be logged in to view this page",
        "bg": "Трябва да сте влезли в системата, за да видите тази страница",
    },
    "nopermtoviewthisview": {
        "en": "You don't have permission to view this file",
        "bg": "Нямате право да преглеждате този файл",
    },
    "tasknotfound": {
        "en": "Task not found",
        "bg": "Задачата не е намерена",
    },
    "nocontent": {
        "en": "No content",
        "bg": "Няма съдържание",

    },
    "toolong20kmax": {
        "en": "Too long. Max 20000 characters",
        "bg": "Твърде дълго. Максимум 20000 символа",
    },
    "nofileselected": {
        "en": "No file selected",
        "bg": "Няма избран файл",
    },
    "Max file size is 15MB": {
        "en": "Max file size is 15MB",
        "bg": "Максималният размер на файла е 15MB",
    },
    "wecannotacceptthisfiletype": {
        "en": "We cannot accept this file type",
        "bg": "Не можем да приемем този тип файл",
    },
    "invalidtype": {
        "en": "Invalid Format. Allowed file types are txt, pdf, png, jpg, jpeg, gif",
        "bg": "Невалиден формат. Позволените типове файлове са txt, pdf, png, jpg, jpeg, gif",
    },
    "workernotfound": {
        "en": "Еmployee not found",
        "bg": "Служителят не е намерен",
    },
    "loggedinsuccess": {
        "en": "Logged in successfully",
        "bg": "Успешно влязохте в системата",
    },
    "incorrectpass": {
        "en": "Incorrect password, try again",
        "bg": "Грешна парола, опитайте отново",
    },
    "emailnotfound": {
        "en": "Email not found",
        "bg": "Имейлът не е намерен",
    },
    "loggedoutsuccess": {
        "en": "Logged out successfully",
        "bg": "Успешно излязохте от системата",
    },
    "captchawrong": {
        "en": "Captcha wrong",
        "bg": "Капчата е грешна",
    },
    "tasklifymedomainnotallowed": {
        "en": "Tasklify.me cannot be used as a domain for email",
        "bg": "Tasklify.me не може да се използва като домейн за имейл",
    },
    "emailalreadyexists": {
        "en": "Email already exists",
        "bg": "Имейлът вече съществува",
    },
    "emailtooshort": {
        "en": "Email too short",
        "bg": "Имейлът е твърде къс",
    },
    "nametooshort": {
        "en": "Name too short",
        "bg": "Името е твърде късо",
    },
    "passwordtooshort": {
        "en": "Password too short. At least 8 characters",
        "bg": "Паролата е твърде къса. Поне 8 символа",
    },
    "passwordsdontmatch": {
        "en": "Passwords don't match",
        "bg": "Паролите не съвпадат",
    },
    "accountcreated": {
        "en": "Account created",
        "bg": "Акаунта е създаден",
    },
    "youhaveworkerscannotdelete": {
        "en": "You have employees, you cannot delete your account",
        "bg": "Имате служители, не можете да изтриете акаунта си",
    },
    "accontdeletesuccess": {
        "en": "Account deleted successfully",
        "bg": "Акаунта е изтрит успешно",
    },
    "youmustconfirmdelete": {
        "en": "You must confirm deletion of your account",
        "bg": "Трябва да потвърдите изтриването на акаунта си",
    },
    "mustconfirmchangepassword": {
        "en": "You must confirm change of your password",
        "bg": "Трябва да потвърдите промяната на паролата си",
    },
    "passwordchangedsuccess": {
        "en": "Password changed successfully",
        "bg": "Паролата е променена успешно",
    },
    "profilenav": {
        "en": "Profile",
        "bg": "Профил",
    },
    "loginnav": {
        "en": "Login",
        "bg": "Вход",
    },
    "signupnav": {
        "en": "Sign up",
        "bg": "Регистрация",
    },
    "tasksnav": {
        "en": "Tasks",
        "bg": "Задачи",
    },
    "workersnav": {
        "en": "Employees",
        "bg": "Служители",
    },
    "adminnav": {
        "en": "Admin",
        "bg": "Админ",
    },
    "logoutnav": {
        "en": "Logout",
        "bg": "Изход",
    },
    "homenav": {
        "en": "Home",
        "bg": "Начало",
    },
    "signupemploy": {
        "en": "Sign up your employee",
        "bg": "Регистрирайте служителя си",
    },
    "addemployeeinfosignup": {
        "en": 'You need to input this code in page "Employees", section "Add Employee"',
        "bg": 'Трябва да въведете този код на страницата "Служители", секция "Добави служител"',
    },
    "employreccode": {
        "en": "Your employee will receive confirmation email with registraion code",
        "bg": "Служителят ви ще получи имейл за потвърждение с код за регистрация",
    }, }



def getword(word, target):
    if target not in ["en", "bg"]:
        return "Invalid language"
    if word in words:
        if target in words[word]:
            return words[word][target]
        else:
            return "!!! No translation for " + target + " !!!"
    else:
        return "!!! WORD NOT FOUND !!! " + word

def loadtime():
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)
    return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())


loadtime()


