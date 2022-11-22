from flask import request, current_app, render_template, redirect, url_for, flash, session, jsonify
from flask_login import current_user, login_required
import time
words = {

    "email": {
        "en": "Email Address",
        "bg": "Електронна поща",
        "es": "Correo electrónico",
        "de": "E-Mail-Adresse",
        "fr": "Adresse e-mail",
        "ru": "Электронная почта"
    },
    "emailshort": {
        "en": "Email",
        "bg": "Ел. поща",
        "es": "Correo",
        "de": "E-Mail",
        "fr": "Email",
        "ru": "Эл. почта"
    },
    "password": {
        "en": "Password",
        "bg": "Парола",
        "es": "Contraseña",
        "de": "Passwort",
        "fr": "Mot de passe",
        "ru": "Пароль"
    },
    "enteremail": {
        "en": "Enter Email",
        "bg": "Въведете имейл",
        "es": "Introduzca el correo electrónico",
        "de": "E-Mail eingeben",
        "fr": "Entrez l'email",
        "ru": "Введите адрес электронной почты"
    },
    "login": {
        "en": "Login",
        "bg": "Вход",
        "es": "Iniciar sesión",
        "de": "Anmeldung",
        "fr": "S'identifier",
        "ru": "Войти"
    },
    "profiletext": {
        "en": "Profile",
        "bg": "Профил",
        "es": "Perfil",
        "de": "Profil",
        "fr": "Profil",
        "ru": "Профиль"
    },
    "name": {
        "en": "Name",
        "bg": "Име",
        "es": "Nombre",
        "de": "Name",
        "fr": "Nom",
        "ru": "Имя"
    },
    "changepassword": {
        "en": "Change Password",
        "bg": "Смяна на парола",
        "es": "Cambia la contraseña",
        "de": "Passwort ändern",
        "fr": "Changer le mot de passe",
        "ru": "Сменить пароль"
    },
    "deleteaccount": {
        "en": "Delete Account",
        "bg": "Изтриване на акаунт",
        "es": "Eliminar cuenta",
        "de": "Konto löschen",
        "fr": "Supprimer le compte",
        "ru": "Удалить аккаунт"
    },
    "oldpassword": {
        "en": "Old Password",
        "bg": "Стара парола",
        "es": "Contraseña anterior",
        "de": "Altes Passwort",
        "fr": "Ancien mot de passe",
        "ru": "Старый пароль"
    },
    "newpassword": {
        "en": "New Password",
        "bg": "Нова парола",
        "es": "Nueva contraseña",
        "de": "Neues Kennwort",
        "fr": "Nouveau mot de passe",
        "ru": "Новый пароль"
    },
    "cnewpassword": {
        "en": "Confirm Password",
        "bg": "Потвърдете паролата",
        "es": "Confirmar contraseña",
        "de": "Kennwort bestätigen",
        "fr": "Confirmez le mot de passe",
        "ru": "Подтвердите пароль"
    },
    "confirm": {
        "en": "By checking this box and clicking the 'change password' button, you agree that you want to change your account password, making the old password invalid immediately after clicking the button.",
        "bg": "Отмятайки тази кутийка и натискайки бутона 'Смяна на парола', за да потвърдите, че искате да смените паролата си, като старата парола става невалидна веднага след натискането на бутона.",
        "es": "Al marcar esta casilla y hacer clic en el botón 'Cambiar contraseña', acepta que desea cambiar la contraseña de su cuenta, haciendo que la contraseña anterior sea inválida inmediatamente después de hacer clic en el botón.",
        "de": "Wenn Sie dieses Kontrollkästchen aktivieren und auf die Schaltfläche 'Passwort ändern' klicken, stimmen Sie zu, dass Sie Ihr Konto-Passwort ändern möchten, wodurch das alte Passwort sofort nach dem Klicken auf die Schaltfläche ungültig wird.",
        "fr": "En cochant cette case et en cliquant sur le bouton 'Changer le mot de passe', vous acceptez que vous souhaitez modifier votre mot de passe de compte, rendant l'ancien mot de passe invalide immédiatement après avoir cliqué sur le bouton.",
        "ru": "Отметив этот флажок и нажав кнопку «Сменить пароль», вы соглашаетесь, что хотите изменить пароль своей учетной записи, сделав старый пароль недействительным сразу после нажатия кнопки."
    },
    "enterpassword": {
        "en": "Enter Password",
        "bg": "Въведете парола",
        "es": "Introduzca la contraseña",
        "de": "Passwort eingeben",
        "fr": "Entrez le mot de passe",
        "ru": "Введите пароль"
    },
    "confirmdelete": {
        "en": "By checking this box and clicking the 'delete account' button, you agree that you want to delete your account, making it impossible to recover it.",
        "bg": "Отмятайки тази кутийка и натискайки бутона 'Изтриване на акаунт', за да потвърдите, че искате да изтриете акаунта си, като той става невъзможен за възстановяване.",
        "es": "Al marcar esta casilla y hacer clic en el botón 'Eliminar cuenta', acepta que desea eliminar su cuenta, haciendo que sea imposible recuperarla.",
        "de": "Wenn Sie dieses Kontrollkästchen aktivieren und auf die Schaltfläche 'Konto löschen' klicken, stimmen Sie zu, dass Sie Ihr Konto löschen möchten, wodurch es unmöglich ist, es wiederherzustellen.",
        "fr": "En cochant cette case et en cliquant sur le bouton 'Supprimer le compte', vous acceptez que vous souhaitez supprimer votre compte, ce qui rend impossible de le récupérer.",
        "ru": "Отметив этот флажок и нажав кнопку «Удалить аккаунт», вы соглашаетесь, что хотите удалить свою учетную запись, сделав ее невозможным для восстановления."
    },
    "submit": {
        "en": "Submit",
        "bg": "Изпрати",
        "es": "Enviar",
        "de": "einreichen",
        "fr": "Soumettre",
        "ru": "Отправить"
    },
    "firstandlast": {
        "en": "First and Last Name",
        "bg": "Име и фамилия",
        "es": "Nombre y apellido",
        "de": "Vor- und Nachname",
        "fr": "Prénom et nom de famille",
        "ru": "Имя и фамилия"
    },
    "signup": {
        "en": "Sign Up",
        "bg": "Регистрация",
        "es": "Regístrate",
        "de": "Anmelden",
        "fr": "S'inscrire",
        "ru": "Зарегистрироваться"
    },
    "alreadyhaveaccount": {
        "en": "Already have an account?",
        "bg": "Вече имате акаунт?",
        "es": "¿Ya tienes una cuenta?",
        "de": "Hast du schon ein Konto?",
        "fr": "Vous avez déjà un compte?",
        "ru": "Уже есть аккаунт?"
    },
    "loginhere": {
        "en": "Login here",
        "bg": "Влезте тук",
        "es": "Inicia sesión aquí",
        "de": "Hier anmelden",
        "fr": "Connectez-vous ici",
        "ru": "Войдите здесь"
    },
    "logout": {
        "en": "Logout",
        "bg": "Изход",
        "es": "Cerrar sesión",
        "de": "Ausloggen",
        "fr": "Se déconnecter",
        "ru": "Выйти"
    },
    "registerhere": {
        "en": "Register here",
        "bg": "Регистрирайте се тук",
        "es": "Regístrate aquí",
        "de": "Hier registrieren",
        "fr": "Inscrivez-vous ici",
        "ru": "Зарегистрируйтесь здесь"
    },
    "notregistered": {
        "en": "Not registered?",
        "bg": "Не сте регистрирани?",
        "es": "¿No estás registrado?",
        "de": "Nicht registriert?",
        "fr": "Pas enregistré?",
        "ru": "Не зарегистрированы?"
    },
    "boss": {
        "en": "Boss",
        "bg": "Шеф",
        "es": "Jefe",
        "de": "Chef",
        "fr": "Patron",
        "ru": "Босс"
    },
    "accessmessage": {
        "en": "In order to access any other page, your boss must register you first.",
        "bg": "За да имате достъп до други страници, шефът ви трябва да ви регистрира първо.",
        "es": "Para acceder a cualquier otra página, su jefe debe registrarlo primero.",
        "de": "Um auf eine andere Seite zuzugreifen, muss Ihr Chef Sie zuerst registrieren.",
        "fr": "Afin d'accéder à toute autre page, votre patron doit vous enregistrer en premier.",
        "ru": "Чтобы получить доступ к любой другой странице, ваш босс должен сначала зарегистрировать вас."
    },
    "youridtext": {
        "en": "Your ID. Give it to your boss, so he can register you.",
        "bg": "Вашият ID. Дайте го на шефа си, за да ви регистрира.",
        "es": "Su ID. Dígale a su jefe para que pueda registrarlo.",
        "de": "Ihre ID. Geben Sie es Ihrem Chef, damit er Sie registrieren kann.",
        "fr": "Votre ID. Donnez-le à votre patron, afin qu'il puisse vous enregistrer.",
        "ru": "Ваш ID. Дайте его своему боссу, чтобы он мог зарегистрировать вас."
    },
    "delete": {
        "en": "Delete",
        "bg": "Изтрий",
        "es": "Borrar",
        "de": "Löschen",
        "fr": "Effacer",
        "ru": "Удалить"
    },
    "add": {
        "en": "Add",
        "bg": "Добави",
        "es": "Añadir",
        "de": "Hinzufügen",
        "fr": "Ajouter",
        "ru": "Добавить"
    },
    "tasktext": {
        "en": "Task",
        "bg": "Задача",
        "es": "Tarea",
        "de": "Aufgabe",
        "fr": "Tâche",
        "ru": "Задача"
    },
    "statustext": {
        "en": "Status",
        "bg": "Статус",
        "es": "Estado",
        "de": "Status",
        "fr": "Statut",
        "ru": "Статус"
    },
    "workertext": {
        "en": "Employee",
        "bg": "Служител",
        "es": "Empleado",
        "de": "Mitarbeiter",
        "fr": "Employé",
        "ru": "Сотрудник"
    },
    "done": {
        "en": "Done",
        "bg": "Готово",
        "es": "Hecho",
        "de": "Erledigt",
        "fr": "Terminé",
        "ru": "Готово"
    },
    "tasktextplural": {
        "en": "Tasks",
        "bg": "Задачи",
        "es": "Tareas",
        "de": "Aufgaben",
        "fr": "Tâches",
        "ru": "Задачи"
    },
    "NotStarted": {
        "en": "Not Started",
        "bg": "Не е започната",
        "es": "No iniciado",
        "de": "Nicht begonnen",
        "fr": "Pas commencé",
        "ru": "Не начато"
    },
    "completed": {
        "en": "Completed",
        "bg": "Завършена",
        "es": "Completado",
        "de": "Abgeschlossen",
        "fr": "Terminé",
        "ru": "Завершено"
    },
    "addtask": {
        "en": "Add Task",
        "bg": "Добави задача",
        "es": "Añadir tarea",
        "de": "Aufgabe hinzufügen",
        "fr": "Ajouter une tâche",
        "ru": "Добавить задачу"
    },
    "selectall": {
        "en": "Select All",
        "bg": "Избери всички",
        "es": "Seleccionar todo",
        "de": "Alles auswählen",
        "fr": "Tout sélectionner",
        "ru": "Выбрать все"
    },
    "deselectall": {
        "en": "Deselect All",
        "bg": "Отмени избора",
        "es": "Deseleccionar todo",
        "de": "Alles abwählen",
        "fr": "Tout désélectionner",
        "ru": "Отменить выбор"
    },
    "workermenu": {
        "en": "Employee Menu",
        "bg": "Меню на служител",
        "es": "Menú de empleado",
        "de": "Mitarbeiter-Menü",
        "fr": "Menu de l'employé",
        "ru": "Меню сотрудника"
    },
    "moreinfo": {
        "en": "More Info",
        "bg": "Повече информация",
        "es": "Más información",
        "de": "Mehr Info",
        "fr": "Plus d'informations",
        "ru": "Больше информации"
    },
    "tasktitle": {
        "en": "Task Title",
        "bg": "Заглавие на задачата",
        "es": "Título de la tarea",
        "de": "Aufgaben Titel",
        "fr": "Titre de la tâche",
        "ru": "Название задачи"
    },
    "notdone": {
        "en": "Not Done",
        "bg": "Не е готово",
        "es": "No hecho",
        "de": "Nicht erledigt",
        "fr": "Pas terminé",
        "ru": "Не готово"
    },
    "selectworkers": {
        "en": "Select Employees",
        "bg": "Избери служители",
        "es": "Seleccionar empleados",
        "de": "Mitarbeiter auswählen",
        "fr": "Sélectionner les employés",
        "ru": "Выбрать сотрудников"
    },
    "idtext": {
        "en": "ID",
        "bg": "ID",
        "es": "ID",
        "de": "ID",
        "fr": "ID",
        "ru": "ID"
    },
    "addworker": {
        "en": "Add Employee",
        "bg": "Добави служител",
        "es": "Añadir empleado",
        "de": "Mitarbeiter hinzufügen",
        "fr": "Ajouter un employé",
        "ru": "Добавить сотрудника"
    },
    "youllberedirectedto": {
        "en": "You'll be redirected to",
        "bg": "Ще бъдете пренасочени към",
        "es": "Serás redirigido a",
        "de": "Sie werden weitergeleitet zu",
        "fr": "Vous serez redirigé vers",
        "ru": "Вы будете перенаправлены на"
    },
    "infiveseconds": {
        "en": "in 5 seconds",
        "bg": "след 5 секунди",
        "es": "en 5 segundos",
        "de": "in 5 Sekunden",
        "fr": "dans 5 secondes",
        "ru": "через 5 секунд"
    },
    "oryoucango": {
        "en": "or you can go to",
        "bg": "или можете да отидете на",
        "es": "o puedes ir a",
        "de": "oder Sie können zu gehen",
        "fr": "ou vous pouvez aller à",
        "ru": "или вы можете перейти на"
    },
    "here": {
        "en": "Click here",
        "bg": "Натиснете тук",
        "es": "Haga clic aquí",
        "de": "Klicken Sie hier",
        "fr": "Cliquez ici",
        "ru": "Нажмите здесь"
    },
    "myfiles": {
        "en": "My Files",
        "bg": "Моите файлове",
        "es": "Mis archivos",
        "de": "Meine Dateien",
        "fr": "Mes fichiers",
        "ru": "Мои файлы"
    },
    "empmyfiles": {
        "en": "Employee Files",
        "bg": "Файлове на служител",
        "es": "Archivos de empleados",
        "de": "Mitarbeiterdateien",
        "fr": "Fichiers d'employés",
        "ru": "Файлы сотрудника"
    },
    "home": {
        "en": "home",
        "bg": "начало",
        "es": "casa",
        "de": "Zuhause",
        "fr": "maison",
        "ru": "домой"
    },
    "thirdpartylink": {
        "en": "Please note that this is a third party link and we are not responsible for its content.",
        "bg": "Моля, имайте предвид, че това е връзка на трета страна и не сме отговорни за нейното съдържание.",
        "es": "Tenga en cuenta que se trata de un enlace de terceros y no somos responsables de su contenido.",
        "de": "Bitte beachten Sie, dass dies ein Link von Drittanbietern ist und wir für den Inhalt nicht verantwortlich sind.",
        "fr": "Veuillez noter que c'est un lien tiers et nous ne sommes pas responsables de son contenu.",
        "ru": "Обратите внимание, что это ссылка третьей стороны, и мы не несем ответственности за ее содержание."
    },
    "ifyourenotredirected": {
        "en": "If you are not redirected automatically,",
        "bg": "Ако не бъдете пренасочени автоматично,",
        "es": "Si no se redirige automáticamente,",
        "de": "Wenn Sie nicht automatisch weitergeleitet werden,",
        "fr": "Si vous n'êtes pas redirigé automatiquement,",
        "ru": "Если вы не будете перенаправлены автоматически,"
    },
    "contact": {
        "en": "Contact",
        "bg": "Контакт",
        "es": "Contacto",
        "de": "Kontakt",
        "fr": "Contact",
        "ru": "Контакт"
    },
    "contactus": {
        "en": "Contact Us",
        "bg": "Свържете се с нас",
        "es": "Contáctenos",
        "de": "Kontaktiere uns",
        "fr": "Contactez nous",
        "ru": "Свяжитесь с нами"
    },
    "contactusmessage": {
        "en": "If you have any questions, please contact us.",
        "bg": "Ако имате въпроси, моля, свържете се с нас.",
        "es": "Si tiene alguna pregunta, póngase en contacto con nosotros.",
        "de": "Wenn Sie Fragen haben, kontaktieren Sie uns bitte.",
        "fr": "Si vous avez des questions, veuillez nous contacter.",
        "ru": "Если у вас есть какие-либо вопросы, пожалуйста, свяжитесь с нами."
    },
    "contactname": {
        "en": "Deyan Vladimirov Nikolov",
        "bg": "Деян Владимиров Николов",
        "es": "Deyan Vladimirov Nikolov",
        "de": "Deyan Vladimirov Nikolov",
        "fr": "Deyan Vladimirov Nikolov",
        "ru": "Деян Владимиров Николов"
    },
    "contactemail": {
        "en": "deyannikolov25@itpg-varna.bg",
        "bg": "deyannikolov25@itpg-varna.bg",
        "es": "deyannikolov25@itpg-varna.bg",
        "de": "deyannikolov25@itpg-varna.bg",
        "fr": "deyannikolov25@itpg-varna.bg",
        "ru": "deyannikolov25@itpg-varna.bg",
    },
    "databeingproccessed": {
        "en": "Your data is being processed. Please wait and do not refresh the page.",
        "bg": "Вашите данни се обработват. Моля, изчакайте и не актуализирайте страницата.",
        "es": "Sus datos están siendo procesados. Por favor, espere y no actualice la página.",
        "de": "Ihre Daten werden verarbeitet. Bitte warten Sie und aktualisieren Sie die Seite nicht.",
        "fr": "Vos données sont en cours de traitement. Veuillez patienter et ne pas actualiser la page.",
        "ru": "Ваши данные обрабатываются. Пожалуйста, подождите и не обновляйте страницу."
    },
    "print": {
        "en": "Print",
        "bg": "Печат",
        "es": "Impresión",
        "de": "Drucken",
        "fr": "Impression",
        "ru": "Печать"
    },
    "workeridtext": {
        "en": "Employee ID",
        "bg": "ID на служител",
        "es": "ID de empleado",
        "de": "Mitarbeiter-ID",
        "fr": "ID d'employé",
        "ru": "ID сотрудника"
    },
    "workeremailtext": {
        "en": "Employee Email",
        "bg": "Имейл на служител",
        "es": "Correo electrónico del empleado",
        "de": "Mitarbeiter-E-Mail",
        "fr": "Email de l'employé",
        "ru": "Электронная почта сотрудника"
    },
    "workernametext": {
        "en": "Employee Name",
        "bg": "Име на служител",
        "es": "Nombre del empleado",
        "de": "Name des Mitarbeiters",
        "fr": "Nom de l'employé",
        "ru": "Имя сотрудника"
    },
    "taskstatustext": {
        "en": "Task Status",
        "bg": "Статус на задачата",
        "es": "Estado de la tarea",
        "de": "Aufgabenstatus",
        "fr": "Statut de la tâche",
        "ru": "Статус задачи"
    },
    "requestedbytext": {
        "en": "Requested By",
        "bg": "Заявена от",
        "es": "Solicitado por",
        "de": "Angefordert von",
        "fr": "Demandé par",
        "ru": "Запрошено"
    },
    "attext": {
        "en": "at",
        "bg": "в",
        "es": "en",
        "de": "bei",
        "fr": "à",
        "ru": "в"
    },
    "submitcodetext": {
        "en": "You can submit your code through here to get a shareable link.",
        "bg": "Можете да представите своя код чрез тук, за да получите връзка, която можете да споделите.",
        "es": "Puede enviar su código a través de aquí para obtener un enlace compartible.",
        "de": "Sie können Ihren Code hier einreichen, um einen freigegebenen Link zu erhalten.",
        "fr": "Vous pouvez soumettre votre code ici pour obtenir un lien partageable.",
        "ru": "Вы можете отправить свой код здесь, чтобы получить общедоступную ссылку."
    },
    "sevendaylimit": {
        "en": "Your code will be available at this link for 7 days. After that, it will be deleted automatically.",
        "bg": "Вашият код ще бъде наличен на тази връзка за 7 дни. След това ще бъде изтрит автоматично.",
        "es": "Su código estará disponible en este enlace durante 7 días. Después de eso, se eliminará automáticamente.",
        "de": "Ihr Code wird an diesem Link für 7 Tage verfügbar sein. Danach wird er automatisch gelöscht.",
        "fr": "Votre code sera disponible à ce lien pendant 7 jours. Après cela, il sera supprimé automatiquement.",
        "ru": "Ваш код будет доступен по этой ссылке в течение 7 дней. После этого он будет автоматически удален."
    },
    "copy": {
        "en": "Copy",
        "bg": "Копирай",
        "es": "Copiar",
        "de": "Kopieren",
        "fr": "Copier",
        "ru": "Копировать"
    },
    "photouploader": {
        "en": "Photo Uploader",
        "bg": "Качване на снимка",
        "es": "Cargador de fotos",
        "de": "Foto Uploader",
        "fr": "Téléchargeur de photos",
        "ru": "Загрузчик фотографий"
    },
    "markyourtaskasdonetext": {
        "en": "Add any photo link, code link or personal comments in the field and mark your task as done.",
        "bg": "Добавете връзка за снимка, връзка за код или лични коментари в полето и маркирайте задачата си като изпълнена.",
        "es": "Agregue cualquier enlace de foto, enlace de código o comentarios personales en el campo y marque su tarea como completada.",
        "de": "Fügen Sie in das Feld einen beliebigen Foto-Link, einen Code-Link oder persönliche Kommentare hinzu und markieren Sie Ihre Aufgabe als erledigt.",
        "fr": "Ajoutez tout lien photo, lien de code ou commentaires personnels dans le champ et marquez votre tâche comme terminée.",
        "ru": "Добавьте любую ссылку на фото, ссылку на код или личные комментарии в поле и отметьте задачу как выполненную."
    },
    "photolinktexttitle": {
        "en": "Photo Link",
        "bg": "Връзка за снимка",
        "es": "Enlace de foto",
        "de": "Fotolink",
        "fr": "Lien photo",
        "ru": "Ссылка на фото"
    },
    "idemail": {
        "en": "Your registration ID was sent to your email.",
        "bg": "Вашият регистрационен ID беше изпратен на вашия имейл.",
        "es": "Su ID de registro se envió a su correo electrónico.",
        "de": "Ihre Registrierungs-ID wurde an Ihre E-Mail gesendet.",
        "fr": "Votre ID d'enregistrement a été envoyé à votre email.",
        "ru": "Ваш идентификатор регистрации был отправлен на ваш адрес электронной почты."
    },
    "starttext": {
        "en": "Start",
        "bg": "Старт",
        "es": "Comienzo",
        "de": "Anfang",
        "fr": "Début",
        "ru": "Начало"
    },
    "started": {
        "en": "Started",
        "bg": "Стартиран",
        "es": "Comenzado",
        "de": "Gestartet",
        "fr": "Commencé",
        "ru": "Начат"
    },
    "deletefromall": {
        "en": "Delete this task from all employees",
        "bg": "Изтрий тази задача от всички служители",
        "es": "Eliminar esta tarea de todos los empleados",
        "de": "Löschen Sie diese Aufgabe von allen Mitarbeitern",
        "fr": "Supprimer cette tâche de tous les employés",
        "ru": "Удалить эту задачу со всех сотрудников"
    },
    "missingid": {
        "en": "Missing ID",
        "bg": "Липсващ ID",
        "es": "ID faltante",
        "de": "Fehlende ID",
        "fr": "ID manquant",
        "ru": "Отсутствует идентификатор"
    },
    "noworkerwithid": {
        "en": "No employee with that ID",
        "bg": "Няма работник с този ID",
        "es": "No hay empleado con ese ID",
        "de": "Kein Mitarbeiter mit dieser ID",
        "fr": "Aucun employé avec cet ID",
        "ru": "Нет сотрудника с таким идентификатором"
    },
    "workeradded": {
        "en": "Еmployee added",
        "bg": "Служител добавен",
        "es": "Empleado agregado",
        "de": "Mitarbeiter hinzugefügt",
        "fr": "Employé ajouté",
        "ru": "Сотрудник добавлен"
    },
    "workeralreadyremoved": {
        "en": "Employee already removed",
        "bg": "Служителът вече е премахнат",
        "es": "Empleado ya eliminado",
        "de": "Mitarbeiter bereits entfernt",
        "fr": "Employé déjà supprimé",
        "ru": "Сотрудник уже удален"
    },
    "workerremoved": {
        "en": "Employee removed",
        "bg": "Служител премахнат",
        "es": "Empleado eliminado",
        "de": "Mitarbeiter entfernt",
        "fr": "Employé supprimé",
        "ru": "Сотрудник удален"
    },
    "workeralreadyadded": {
        "en": "Employee already added",
        "bg": "Служителът вече е добавен",
        "es": "Empleado ya agregado",
        "de": "Mitarbeiter bereits hinzugefügt",
        "fr": "Employé déjà ajouté",
        "ru": "Сотрудник уже добавлен"
    },
    "missingtask": {
        "en": "Missing task",
        "bg": "Липсваща задача",
        "es": "Tarea faltante",
        "de": "Fehlende Aufgabe",
        "fr": "Tâche manquante",
        "ru": "Отсутствует задача"
    },
    "noworkersselected": {
        "en": "No employees selected",
        "bg": "Няма избрани служители",
        "es": "No hay empleados seleccionados",
        "de": "Keine Mitarbeiter ausgewählt",
        "fr": "Aucun employé sélectionné",
        "ru": "Не выбраны сотрудники"
    },
    "taskadded": {
        "en": "Task added",
        "bg": "Задачата е добавена",
        "es": "Tarea agregada",
        "de": "Aufgabe hinzugefügt",
        "fr": "Tâche ajoutée",
        "ru": "Задача добавлена"
    },
    "youcantedittask": {
        "en": "You can't edit this task",
        "bg": "Не можете да редактирате тази задача",
        "es": "No puedes editar esta tarea",
        "de": "Sie können diese Aufgabe nicht bearbeiten",
        "fr": "Vous ne pouvez pas modifier cette tâche",
        "ru": "Вы не можете редактировать эту задачу"
    },
    "youneedtobeloggedin": {
        "en": "You need to be logged in to view this page",
        "bg": "Трябва да сте влезли в системата, за да видите тази страница",
        "es": "Debe iniciar sesión para ver esta página",
        "de": "Sie müssen angemeldet sein, um diese Seite anzuzeigen",
        "fr": "Vous devez être connecté pour voir cette page",
        "ru": "Вы должны войти в систему, чтобы просмотреть эту страницу"
    },
    "nopermtoviewthisview": {
        "en": "You don't have permission to view this file",
        "bg": "Нямате право да преглеждате този файл",
        "es": "No tiene permiso para ver este archivo",
        "de": "Sie haben keine Berechtigung, diese Datei anzuzeigen",
        "fr": "Vous n'avez pas la permission de voir ce fichier",
        "ru": "У вас нет разрешения на просмотр этого файла"
    },
    "tasknotfound": {
        "en": "Task not found",
        "bg": "Задачата не е намерена",
        "es": "Tarea no encontrada",
        "de": "Aufgabe nicht gefunden",
        "fr": "Tâche introuvable",
        "ru": "Задача не найдена"
    },
    "nocontent": {
        "en": "No content",
        "bg": "Няма съдържание",
        "es": "Sin contenido",
        "de": "Kein Inhalt",
        "fr": "Pas de contenu",
        "ru": "Нет содержимого"

    },
    "toolong20kmax": {
        "en": "Too long. Max 20000 characters",
        "bg": "Твърде дълго. Максимум 20000 символа",
        "es": "Demasiado largo. Máximo 20000 caracteres",
        "de": "Zu lang. Max. 20000 Zeichen",
        "fr": "Trop long. Max 20000 caractères",
        "ru": "Слишком длинный. Максимум 20000 символов"

    },
    "nofileselected": {
        "en": "No file selected",
        "bg": "Няма избран файл",
        "es": "No hay archivo seleccionado",
        "de": "Keine Datei ausgewählt",
        "fr": "Aucun fichier sélectionné",
        "ru": "Файл не выбран"
    },
    "Max file size is 15MB": {
        "en": "Max file size is 15MB",
        "bg": "Максималният размер на файла е 15MB",
        "es": "El tamaño máximo del archivo es de 15MB",
        "de": "Maximale Dateigröße ist 15MB",
        "fr": "La taille maximale du fichier est de 15 Mo",
        "ru": "Максимальный размер файла 15MB"
    },
    "wecannotacceptthisfiletype": {
        "en": "We cannot accept this file type",
        "bg": "Не можем да приемем този тип файл",
        "es": "No podemos aceptar este tipo de archivo",
        "de": "Wir können diesen Dateityp nicht akzeptieren",
        "fr": "Nous ne pouvons pas accepter ce type de fichier",
        "ru": "Мы не можем принять этот тип файла"
    },
    "invalidtype": {
        "en": "Invalid Format.",
        "bg": "Невалиден формат.",
        "es": "Formato inválido.",
        "de": "Ungültiges Format.",
        "fr": "Format invalide.",
        "ru": "Неверный формат."
    },
    "workernotfound": {
        "en": "Еmployee not found",
        "bg": "Служителят не е намерен",
        "es": "Empleado no encontrado",
        "de": "Mitarbeiter nicht gefunden",
        "fr": "Employé introuvable",
        "ru": "Сотрудник не найден"
    },
    "loggedinsuccess": {
        "en": "Logged in successfully",
        "bg": "Успешно влязохте в системата",
        "es": "Inició sesión correctamente",
        "de": "Erfolgreich angemeldet",
        "fr": "Connecté avec succès",
        "ru": "Успешный вход"
    },
    "incorrectpass": {
        "en": "Incorrect password, try again",
        "bg": "Грешна парола, опитайте отново",
        "es": "Contraseña incorrecta, inténtalo de nuevo",
        "de": "Falsches Passwort, versuchen Sie es erneut",
        "fr": "Mot de passe incorrect, réessayez",
        "ru": "Неверный пароль, попробуйте еще раз"
    },
    "emailnotfound": {
        "en": "Email not found",
        "bg": "Имейлът не е намерен",
        "es": "Correo electrónico no encontrado",
        "de": "E-Mail nicht gefunden",
        "fr": "Email introuvable",
        "ru": "Email не найден"
    },
    "loggedoutsuccess": {
        "en": "Logged out successfully",
        "bg": "Успешно излязохте от системата",
        "es": "Cerró sesión correctamente",
        "de": "Erfolgreich abgemeldet",
        "fr": "Déconnecté avec succès",
        "ru": "Успешный выход"
    },
    "captchawrong": {
        "en": "Captcha wrong",
        "bg": "Капчата е грешна",
        "es": "Captcha incorrecta",
        "de": "Captcha falsch",
        "fr": "Captcha incorrect",
        "ru": "Капча неверна"
    },
    "tasklifymedomainnotallowed": {
        "en": "Tasklify.me cannot be used as a domain for email",
        "bg": "Tasklify.me не може да се използва като домейн за имейл",
        "es": "Tasklify.me no se puede usar como dominio para el correo electrónico",
        "de": "Tasklify.me kann nicht als Domain für E-Mails verwendet werden",
        "fr": "Tasklify.me ne peut pas être utilisé comme domaine pour l'email",
        "ru": "Tasklify.me не может быть использовано как домен для электронной почты"
    },
    "emailalreadyexists": {
        "en": "Email already exists",
        "bg": "Имейлът вече съществува",
        "es": "El correo electrónico ya existe",
        "de": "E-Mail existiert bereits",
        "fr": "L'email existe déjà",
        "ru": "Email уже существует"
    },
    "emailtooshort": {
        "en": "Email too short",
        "bg": "Имейлът е твърде къс",
        "es": "Correo electrónico demasiado corto",
        "de": "E-Mail zu kurz",
        "fr": "Email trop court",
        "ru": "Email слишком короткий"
    },
    "nametooshort": {
        "en": "Name too short",
        "bg": "Името е твърде късо",
        "es": "Nombre demasiado corto",
        "de": "Name zu kurz",
        "fr": "Nom trop court",
        "ru": "Имя слишком короткое"
    },
    "passwordtooshort": {
        "en": "Password too short. At least 8 characters",
        "bg": "Паролата е твърде къса. Поне 8 символа",
        "es": "Contraseña demasiado corta. Al menos 8 caracteres",
        "de": "Passwort zu kurz. Mindestens 8 Zeichen",
        "fr": "Mot de passe trop court. Au moins 8 caractères",
        "ru": "Пароль слишком короткий. По крайней мере 8 символов"
    },
    "passwordsdontmatch": {
        "en": "Passwords don't match",
        "bg": "Паролите не съвпадат",
        "es": "Las contraseñas no coinciden",
        "de": "Passwörter stimmen nicht überein",
        "fr": "Les mots de passe ne correspondent pas",
        "ru": "Пароли не совпадают"
    },
    "accountcreated": {
        "en": "Account created",
        "bg": "Акаунта е създаден",
        "es": "Cuenta creada",
        "de": "Konto erstellt",
        "fr": "Compte créé",
        "ru": "Аккаунт создан"
    },
    "youhaveworkerscannotdelete": {
        "en": "You have employees, you cannot delete your account",
        "bg": "Имате служители, не можете да изтриете акаунта си",
        "es": "Tienes empleados, no puedes eliminar tu cuenta",
        "de": "Sie haben Mitarbeiter, Sie können Ihr Konto nicht löschen",
        "fr": "Vous avez des employés, vous ne pouvez pas supprimer votre compte",
        "ru": "У вас есть сотрудники, вы не можете удалить свой аккаунт"
    },
    "accontdeletesuccess": {
        "en": "Account deleted successfully",
        "bg": "Акаунта е изтрит успешно",
        "es": "Cuenta eliminada correctamente",
        "de": "Konto erfolgreich gelöscht",
        "fr": "Compte supprimé avec succès",
        "ru": "Аккаунт успешно удален"
    },
    "youmustconfirmdelete": {
        "en": "You must confirm deletion of your account",
        "bg": "Трябва да потвърдите изтриването на акаунта си",
        "es": "Debe confirmar la eliminación de su cuenta",
        "de": "Sie müssen die Löschung Ihres Kontos bestätigen",
        "fr": "Vous devez confirmer la suppression de votre compte",
        "ru": "Вы должны подтвердить удаление своего аккаунта"
    },
    "mustconfirmchangepassword": {
        "en": "You must confirm change of your password",
        "bg": "Трябва да потвърдите промяната на паролата си",
        "es": "Debe confirmar el cambio de su contraseña",
        "de": "Sie müssen die Änderung Ihres Passworts bestätigen",
        "fr": "Vous devez confirmer le changement de votre mot de passe",
        "ru": "Вы должны подтвердить изменение своего пароля"
    },
    "passwordchangedsuccess": {
        "en": "Password changed successfully",
        "bg": "Паролата е променена успешно",
        "es": "Contraseña cambiada correctamente",
        "de": "Passwort erfolgreich geändert",
        "fr": "Mot de passe changé avec succès",
        "ru": "Пароль успешно изменен"
    },
    "profilenav": {
        "en": "Profile",
        "bg": "Профил",
        "es": "Perfil",
        "de": "Profil",
        "fr": "Profil",
        "ru": "Профиль"
    },
    "loginnav": {
        "en": "Login",
        "bg": "Вход",
        "es": "Iniciar sesión",
        "de": "Anmeldung",
        "fr": "S'identifier",
        "ru": "Вход"
    },
    "signupnav": {
        "en": "Sign up",
        "bg": "Регистрация",
        "es": "Regístrate",
        "de": "Anmelden",
        "fr": "S'inscrire",
        "ru": "Регистрация"
    },
    "tasksnav": {
        "en": "Tasks",
        "bg": "Задачи",
        "es": "Tareas",
        "de": "Aufgaben",
        "fr": "Tâches",
        "ru": "Задачи"
    },
    "workersnav": {
        "en": "Employees",
        "bg": "Служители",
        "es": "Empleados",
        "de": "Mitarbeiter",
        "fr": "Employés",
        "ru": "Сотрудники"
    },
    "adminnav": {
        "en": "Admin",
        "bg": "Админ",
        "es": "Admin",
        "de": "Admin",
        "fr": "Admin",
        "ru": "Админ"
    },
    "logoutnav": {
        "en": "Logout",
        "bg": "Изход",
        "es": "Cerrar sesión",
        "de": "Ausloggen",
        "fr": "Se déconnecter",
        "ru": "Выход"
    },
    "homenav": {
        "en": "Home",
        "bg": "Начало",
        "es": "Casa",
        "de": "Zuhause",
        "fr": "Accueil",
        "ru": "Главная"
    },
    "signupemploy": {
        "en": "Sign up your employee",
        "bg": "Регистрирайте служителя си",
        "es": "Registra a tu empleado",
        "de": "Melden Sie Ihren Mitarbeiter an",
        "fr": "Inscrivez votre employé",
        "ru": "Зарегистрируйте своего сотрудника"
    },
    "addemployeeinfosignup": {
        "en": 'You need to input this code in page "Employees", section "Add Employee"',
        "bg": 'Трябва да въведете този код на страницата "Служители", секция "Добави служител"',
        "es": 'Debe ingresar este código en la página "Empleados", sección "Agregar empleado"',
        "de": 'Sie müssen diesen Code auf der Seite "Mitarbeiter" im Abschnitt "Mitarbeiter hinzufügen" eingeben',
        "fr": 'Vous devez saisir ce code sur la page "Employés", section "Ajouter un employé"',
        "ru": 'Вам необходимо ввести этот код на странице "Сотрудники", раздел "Добавить сотрудника"'
    },
    "employreccode": {
        "en": "Your employee will receive confirmation email with registraion code",
        "bg": "Служителят ви ще получи имейл за потвърждение с код за регистрация",
        "es": "Su empleado recibirá un correo electrónico de confirmación con el código de registro",
        "de": "Ihr Mitarbeiter wird eine Bestätigungs-E-Mail mit Registrierungscode erhalten",
        "fr": "Votre employé recevra un email de confirmation avec le code d'inscription",
        "ru": "Ваш сотрудник получит письмо с кодом подтверждения регистрации"
    },
    "uploadtext": {
        "en": "Upload",
        "bg": "Качи",
        "es": "Subir",
        "de": "Hochladen",
        "fr": "Télécharger",
        "ru": "Загрузить"
    },
    "tooltext1": {
        "en": "Tasklify is a company task allocation tool!",
        "bg": "Tasklify е инструмент за разпределяне на задачи в компания!",
        "es": "Tasklify es una herramienta de asignación de tareas de la empresa!",
        "de": "Tasklify ist ein Aufgabenverteilungstool für Unternehmen!",
        "fr": "Tasklify est un outil d'allocation de tâches pour les entreprises!",
        "ru": "Tasklify - это инструмент распределения задач в компании!"
    },
    "tooltext2": {
        "en": "It's a very good tool for your company!",
        "bg": "Това е много добър инструмент за вашата компания!",
        "es": "¡Es una herramienta muy buena para tu empresa!",
        "de": "Es ist ein sehr gutes Tool für Ihr Unternehmen!",
        "fr": "C'est un très bon outil pour votre entreprise!",
        "ru": "Это очень хороший инструмент для вашей компании!"
    },
    "tooltext3": {
        "en": "If you are interested, sign-up today!",
        "bg": "Ако сте заинтересовани, регистрирайте се днес!",
        "es": "Si estás interesado, ¡regístrate hoy!",
        "de": "Wenn Sie interessiert sind, melden Sie sich heute an!",
        "fr": "Si vous êtes intéressé, inscrivez-vous aujourd'hui!",
        "ru": "Если вы заинтересованы, зарегистрируйтесь сегодня!"
    },
    "goback": {
        "en": "Go back",
        "bg": "Върни се",
        "es": "Volver",
        "de": "Geh zurück",
        "fr": "Retourner",
        "ru": "Вернуться"

    },
    "adminpaneltext": {
        "en": "Admin panel",
        "bg": "Админ панел",
        "es": "Panel de administración",
        "de": "Admin Panel",
        "fr": "Panneau d'administration",
        "ru": "Админ панель"
    },
    "addemployeebutton": {
        "en": "Add employee",
        "bg": "Добави служител",
        "es": "Agregar empleado",
        "de": "Mitarbeiter hinzufügen",
        "fr": "Ajouter un employé",
        "ru": "Добавить сотрудника"
    },
    "registeryouremployee": {
        "en": "Register your employee",
        "bg": "Регистрирайте служителя си",
        "es": "Registra a tu empleado",
        "de": "Melden Sie Ihren Mitarbeiter an",
        "fr": "Inscrivez votre employé",
        "ru": "Зарегистрируйте своего сотрудника"
    },
    "addtasktext": {
        "en": "Add task",
        "bg": "Добави задача",
        "es": "Agregar tarea",
        "de": "Aufgabe hinzufügen",
        "fr": "Ajouter une tâche",
        "ru": "Добавить задачу"
    },
    "actiontext": {
        "en": "Actions",
        "bg": "Действия",
        "es": "Acciones",
        "de": "Aktionen",
        "fr": "Actions",
        "ru": "Действия"
    },
    "signupas": {
        "en": "Sign up as",
        "bg": "Регистрирай се като",
        "es": "Regístrate como",
        "de": "Melde dich an als",
        "fr": "Inscrivez-vous en tant que",
        "ru": "Зарегистрируйтесь как"
    },
    "worker": {
        "en": "Employee",
        "bg": "Служител",
        "es": "Empleado",
        "de": "Mitarbeiter",
        "fr": "Employé",
        "ru": "Сотрудник"
    },
    "due": {
        "en": "Due",
        "bg": "До",
        "es": "Debido",
        "de": "Fällig",
        "fr": "Dû",
        "ru": "До"
    },
    "fileuploader": {
        "en": "File Uploader",
        "bg": "Качване на файл",
        "es": "Cargador de archivos",
        "de": "Datei Uploader",
        "fr": "Téléchargeur de fichiers",
    },
    "dateinpast": {
        "en": "Date is in the past",
        "bg": "Датата е в миналото",
        "es": "La fecha está en el pasado",
        "de": "Datum ist in der Vergangenheit",
        "fr": "La date est dans le passé",
        "ru": "Дата в прошлом"
    },
    "missingdate": {
        "en": "Missing date",
        "bg": "Липсваща дата",
        "es": "Fecha faltante",
        "de": "Fehlendes Datum",
        "fr": "Date manquante",
        "ru": "Отсутствует дата"
    },
    "noworkers": {
        "en": "You have no employees",
        "bg": "Нямате служители",
        "es": "No tienes empleados",
        "de": "Sie haben keine Mitarbeiter",
        "fr": "Vous n'avez pas d'employés",
        "ru": "У вас нет сотрудников"
    },
    "titletext": {
        "en": "Title",
        "bg": "Заглавие",
        "es": "Título",
        "de": "Titel",
        "fr": "Titre",
        "ru": "Заголовок"
    }

}



def getword(word, target):
    if target not in ["en", "bg", "es", "de", "fr", "ru"]:
        return "Error: target language not supported"
    if word in words:
        if target in words[word]:
            return words[word][target]
        else:
            return "!!! No translation for " + target + " and " + word + " !!!"
    else:
        return "!!! WORD NOT FOUND !!! " + word

def loadtime():
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)
    return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())


