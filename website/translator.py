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
        "en": "Employer",
        "bg": "Работодател",
        "es": "Empleador",
        "de": "Arbeitgeber",
        "fr": "Employeur",
        "ru": "Работодатель"
    },
    "accessmessage": {
        "en": "In order to access any other page, your Employer must register you first.",
        "bg": "За да имате достъп до други страници, работодателя ви трябва да ви регистрира първо.",
        "es": "Para acceder a cualquier otra página, su empleador debe registrarlo primero.",
        "de": "Um auf eine andere Seite zuzugreifen, muss Ihr Arbeitgeber Sie zuerst registrieren.",
        "fr": "Afin d'accéder à toute autre page, votre employeur doit vous enregistrer en premier.",
        "ru": "Чтобы получить доступ к любой другой странице, ваш работодатель должен сначала зарегистрировать вас."
    },
    "youridtext": {
        "en": "Your ID. Give it to your еmployer, so he can register you.",
        "bg": "Вашият ID. Дайте го на работодателя си, за да може да ви регистрира.",
        "es": "Su ID. Dígale a su empleador para que pueda registrarlo.",
        "de": "Ihre ID. Geben Sie es Ihrem Arbeitgeber, damit er Sie registrieren kann.",
        "fr": "Votre ID. Donnez-le à votre employeur pour qu'il puisse vous enregistrer.",
        "ru": "Ваш ID. Дайте его вашему работодателю, чтобы он мог зарегистрировать вас."
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
        "bg": "Регистрирай нов служител",
        "es": "Registra a tu empleado",
        "de": "Melden Sie Ihren Mitarbeiter an",
        "fr": "Inscrivez votre employé",
        "ru": "Зарегистрируйте нового сотрудника"
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
    },
    "demoaccount": {
        "en": "Demo accounts cannot be used for login. Please register your own account.",
        "bg": "Демо акаунтите не могат да бъдат използвани за вход. Моля регистрирайте собствен акаунт.",
        "es": "Las cuentas de demostración no se pueden usar para iniciar sesión. Registre su propia cuenta.",
        "de": "Demo-Konten können nicht zum Anmelden verwendet werden. Bitte registrieren Sie Ihr eigenes Konto.",
        "fr": "Les comptes de démonstration ne peuvent pas être utilisés pour la connexion. Veuillez enregistrer votre propre compte.",
        "ru": "Демо-аккаунты не могут использоваться для входа. Пожалуйста, зарегистрируйте свой собствен аккаунт."
    },
    "privacypolicytitle": {
        "en": "Privacy Policy",
        "bg": "Политика за поверителност",
        "es": "Política de privacidad",
        "de": "Datenschutz-Bestimmungen",
        "fr": "Politique de confidentialité",
        "ru": "Политика конфиденциальности"
    },
    "privacypolicytext1": {
        "bg": "е изградил своята политика на дейност като се базира на "
              "уважение към Вашата поверителност по отношение на всички данни, които изискваме от Вас "
              "в нашия уебсайт https://tasklify.me и в други наши сайтове или платоформи, с които оперираме.",
        "es": "ha construido su política de privacidad basándose en el respeto a su privacidad en relación con todos los datos que le pedimos "
              "en nuestro sitio web https://tasklify.me y en otros sitios web o plataformas que operamos.",
        "de": "hat seine Datenschutzrichtlinie aufgebaut, indem er auf den Respekt vor Ihrer Privatsphäre in Bezug auf alle Daten, die wir von Ihnen "
                "auf unserer Website https://tasklify.me und auf anderen Websites oder Plattformen, die wir betreiben, verlangen.",
        "fr": "a construit sa politique de confidentialité en s'appuyant sur le respect de votre vie privée par rapport à toutes les données que nous vous demandons "
                "sur notre site web https://tasklify.me et sur d'autres sites web ou plateformes que nous exploitons.",
        "ru": "создал свою политику конфиденциальности, основываясь на уважении к вашей конфиденциальности по отношению ко всем данным, которые мы запрашиваем у вас "
                "на нашем веб-сайте https://tasklify.me и на других веб-сайтах или платформах, которые мы используем.",
        "en": "has built its privacy policy based on respect for your privacy regarding all data that we request from you "
                "on our website https://tasklify.me and on other websites or platforms that we operate."
    },
    "privacypolicytext2": {
        "bg": "За да Ви предоставим нашата услуга, изискваме от Вас лична информация и то"
              " само, когато действително се нуждаем от нея. Изискваме я по съвсем законен и коректен начин, като предварително"
              " сме Ви уведомили и сме получили Вашето съгласие за събиране на личните Ви данни. Разбира се, ние сме Ви"
              " инфoрмирали защо изискваме и събираме личните Ви данни и как ще ги използваме. ",
        "es": "Para poder ofrecerle nuestro servicio, necesitamos que nos proporcione información personal y solo cuando realmente la necesitemos. "
                " La solicitamos de manera totalmente legal y correcta, previamente le hemos informado y hemos obtenido su consentimiento para recopilar sus datos personales. "
                " Por supuesto, le hemos informado de por qué necesitamos y recopilamos sus datos personales y cómo los utilizaremos.",
        "de": "Um Ihnen unseren Service anbieten zu können, benötigen wir, dass Sie uns persönliche Informationen bereitstellen und dies nur, wenn wir sie wirklich benötigen. "
                " Wir bitten Sie auf rechtlich korrekte und korrekte Weise, und Sie haben uns zuvor darüber informiert und Ihre Zustimmung zur Erfassung Ihrer persönlichen Daten erteilt. "
                " Natürlich haben wir Sie darüber informiert, warum wir Ihre persönlichen Daten benötigen und sammeln und wie wir sie verwenden werden.",
        "fr": "Pour pouvoir vous offrir notre service, nous avons besoin que vous nous fournissiez des informations personnelles et uniquement lorsque nous en avons vraiment besoin. "
                " Nous vous demandons de manière totalement légale et correcte, et vous nous avez informés à l'avance et nous avons obtenu votre consentement pour collecter vos données personnelles. "
                " Bien sûr, nous vous avons informés de pourquoi nous avons besoin et collectons vos données personnelles et comment nous allons les utiliser.",
        "ru": "Чтобы предоставить вам нашу услугу, нам нужна ваша личная информация и только тогда, когда нам действительно нужна эта информация. "
                " Мы просим вас законно и корректно, и вы нам заранее сообщили и дали нам свое согласие на сбор ваших личных данных. "
                " Конечно, мы сообщили вам, почему нам нужны и собираем ваши личные данные и как мы будем их использовать.",
        "en": "To provide you with our service, we need you to provide us with personal information and only when we really need it. "
                " We ask you in a totally legal and correct way, and you have informed us in advance and have given us your consent to collect your personal data. "
                " Of course, we have informed you of why we need and collect your personal data and how we will use it."

    },
    "privacypolicytext3": {
        "bg": "запазва получената от Вас лична информация за толкова"
              " време, което е необходимо да Ви предоставим услугата, която желаете от нас. Данните, които изискваме и запазваме"
              " ще защитаваме с цел избягване на непозволен достъп, разкриване, използване или корекция, копиране. Целта е да не"
              " се допускат загуби и кражби.",
        "es": "guarda la información personal que nos proporciona durante el tiempo que sea necesario para proporcionarle el servicio que solicita. "
                " Los datos que solicitamos y guardamos se protegerán para evitar el acceso no autorizado, divulgación, uso o modificación, copia. "
                " El objetivo es evitar pérdidas y robos.",
        "de": "speichert die von Ihnen bereitgestellten persönlichen Informationen für die Zeit, die für die Bereitstellung des von Ihnen gewünschten Services erforderlich ist. "
                " Die von uns angeforderten und gespeicherten Daten werden geschützt, um einen unautorisierten Zugriff, eine Offenlegung, eine Verwendung oder eine Änderung, eine Kopie zu verhindern. "
                " Das Ziel ist es, Verluste und Diebstähle zu vermeiden.",
        "fr": "garde les informations personnelles que vous nous fournissez pendant le temps nécessaire pour vous fournir le service que vous demandez. "
                " Les données que nous demandons et que nous stockons seront protégées pour éviter l'accès non autorisé, la divulgation, l'utilisation ou la modification, la copie. "
                " L'objectif est d'éviter les pertes et les vols.",
        "ru": "хранит полученную от вас личную информацию на столько времени, сколько необходимо, чтобы предоставить вам услугу, которую вы хотите от нас. "
                " Данные, которые мы запрашиваем и храним, будут защищены для предотвращения неправомерного доступа, раскрытия, использования или изменения, копирования. "
                " Цель - предотвратить потери и кражи.",
        "en": "stores the personal information you provide us for as long as it is necessary to provide you with the service you request. "
                " The data we request and store will be protected to prevent unauthorized access, disclosure, use or modification, copying. "
                " The goal is to prevent losses and thefts."
    },
    "privacypolicytext4": {
        "bg": "не допуска публично споделяне или споделяне с трети страни на"
              " събраната от Вас информация, с изключение на случаите , в които законът го налага.",
        "es": "no permite el acceso público o la divulgación a terceros de la información que nos proporciona, excepto en los casos en que la ley lo exija.",
        "de": "erlaubt keinen öffentlichen Zugriff oder die Weitergabe an Dritte der von Ihnen bereitgestellten Informationen, es sei denn, dies ist gesetzlich vorgeschrieben.",
        "fr": "n'autorise pas l'accès public ou la divulgation à des tiers des informations que vous nous fournissez, sauf dans les cas où la loi l'exige.",
        "ru": "не позволяет публичный доступ или раскрытие третьим лицам информации, которую вы нам предоставляете, за исключением случаев, когда это требуется законом.",
        "en": "does not allow public access or disclosure to third parties of the information you provide us, except in cases where the law requires it."
    },
    "privacypolicytext5": {
        "bg": "осъществява връзка с външни сайтове. Над тях ние нямаме"
              " управление и затова не можем да контролираме тяхното съдържание и действия и съответно нямаме отговорност за"
              " техните политики за поверителност.",
        "es": "está conectado a sitios web externos. No tenemos control sobre ellos y, por lo tanto, no podemos controlar su contenido y acciones y, por lo tanto, no somos responsables de sus políticas de privacidad.",
        "de": "ist mit externen Websites verbunden. Wir haben keinen Einfluss auf sie und können daher ihren Inhalt und ihre Aktionen nicht kontrollieren und sind daher nicht für ihre Datenschutzrichtlinien verantwortlich.",
        "fr": "est connecté à des sites Web externes. Nous n'avons pas de contrôle sur eux et ne pouvons donc pas contrôler leur contenu et leurs actions et ne sommes donc pas responsables de leurs politiques de confidentialité.",
        "ru": "связан с внешними сайтами. Мы не контролируем их и, следовательно, не можем контролировать их содержимое и действия и, следовательно, не несем ответственности за их политики конфиденциальности.",
        "en": "is connected to external websites. We have no control over them and therefore cannot control their content and actions and therefore are not responsible for their privacy policies."
    },
    "privacypolicytext6": {
        "bg": "Ние проявяваме разбиране ако не приемете нашата заявка за личните Ви данни и"
              " лична информация, ако не можем да изпълним услугите, които желаете.",
        "es": "entendemos si no acepta nuestra solicitud de sus datos personales y su información personal, si no podemos cumplir con los servicios que desea.",
        "de": "wir verstehen, wenn Sie unsere Anfrage um Ihre persönlichen Daten und Ihre persönlichen Informationen nicht akzeptieren, wenn wir Ihre gewünschten Dienste nicht erfüllen können.",
        "fr": "nous comprenons si vous n'acceptez pas notre demande de vos données personnelles et de vos informations personnelles, si nous ne pouvons pas fournir les services que vous souhaitez.",
        "ru": "мы понимаем, если вы не примете наш запрос о ваших личных данных и личной информации, если мы не сможем предоставить услуги, которые вы хотите.",
        "en": "we understand if you do not accept our request for your personal data and personal information, if we cannot provide the services you want."
    },
    "privacypolicytext7": {
        "bg": "Ако Вие сте решили да използвате нашия уебсайт и продължите да го правите, това"
              " ще означава, че сте възприели нашите действия и Политика за поверителност за личните данни и лична информация."
              " Без колебание може да се свържете с нас, ако възникнат въпроси по отношение обработването на личните Ви данни и"
              " информация",
        "es": "Si ha decidido utilizar nuestro sitio web y continúa haciéndolo, esto significa que ha aceptado nuestras acciones y nuestra Política de privacidad para sus datos personales y su información personal. No dude en ponerse en contacto con nosotros si tiene alguna pregunta sobre el tratamiento de sus datos personales y su información personal",
        "de": "Wenn Sie sich dazu entschieden haben, unsere Website zu verwenden und sie weiterhin verwenden, bedeutet dies, dass Sie unsere Aktionen und unsere Datenschutzrichtlinie für Ihre persönlichen Daten und Ihre persönlichen Informationen akzeptiert haben. Zögern Sie nicht, uns zu kontaktieren, wenn Sie Fragen zum Umgang mit Ihren persönlichen Daten und Ihren persönlichen Informationen haben",
        "fr": "Si vous avez décidé d'utiliser notre site Web et de continuer à le faire, cela signifie que vous avez accepté nos actions et notre politique de confidentialité pour vos données personnelles et vos informations personnelles. N'hésitez pas à nous contacter si vous avez des questions sur le traitement de vos données personnelles et de vos informations personnelles",
        "ru": "Если вы решили использовать наш веб-сайт и продолжить это делать, это означает, что вы приняли наши действия и нашу политику конфиденциальности по отношению к вашим личным данным и личной информации. Не стесняйтесь обращаться к нам, если у вас есть вопросы по обработке ваших личных данных и личной информации",
        "en": "If you have decided to use our website and continue to do so, this means that you have accepted our actions and our Privacy Policy for your personal data and personal information. Do not hesitate to contact us if you have any questions about the processing of your personal data and personal information"
    },
    "privacypolicytext8": {
        "bg": "Декларацията е актуализирана на 25 декември 2022 г.",
        "es": "La declaración se actualizó el 25 de diciembre de 2022",
        "de": "Die Erklärung wurde am 25. Dezember 2022 aktualisiert",
        "fr": "La déclaration a été mise à jour le 25 décembre 2022",
        "ru": "Декларация обновлена 25 декабря 2022 г.",
        "en": "The statement was updated on December 25, 2022"
    },
    "privacypolicytext9": {
        "bg": "използва услугите на Google OAuth2 за да ви предостави възможност да влезете в профила си чрез вашия Google профил."
              " Ние съхраняваме вашите данни по същия начин както и с обикновената регистрация. Безопасността на вашите данни,"
              " идващи от Google, се контролира от самите Google. Ние не имаме достъп до вашите данни, които са в Google."
              " Можете да прочетете повече за това как Google съхранява вашите данни на следната страница: https://policies.google.com/privacy",
        "es": "utiliza los servicios de Google OAuth2 para proporcionarle la posibilidad de iniciar sesión en su cuenta a través de su perfil de Google."
              " Guardamos sus datos de la misma manera que con el registro normal. La seguridad de sus datos, provenientes de Google,"
              " es controlada por Google. No tenemos acceso a sus datos que están en Google."
              " Puede leer más sobre cómo Google almacena sus datos en la siguiente página: https://policies.google.com/privacy",
        "de": "nutzt die Dienste von Google OAuth2, um Ihnen die Möglichkeit zu geben, sich über Ihr Google-Profil in Ihr Konto einzuloggen."
              " Wir speichern Ihre Daten auf die gleiche Weise wie bei der normalen Registrierung. Die Sicherheit Ihrer Daten, die von Google stammen, wird von Google selbst kontrolliert. Wir haben keinen Zugriff auf Ihre Daten, die in Google sind."
              " Sie können mehr darüber lesen, wie Google Ihre Daten speichert, auf der folgenden Seite: https://policies.google.com/privacy",
        "fr": "utilise les services de Google OAuth2 pour vous permettre de vous connecter à votre compte via votre profil Google."
              " Nous stockons vos données de la même manière que pour l'enregistrement normal. La sécurité de vos données provenant de Google est contrôlée par Google. Nous n'avons pas accès à vos données qui sont dans Google."
              " Vous pouvez en savoir plus sur la façon dont Google stocke vos données sur la page suivante: https://policies.google.com/privacy",
        "ru": "использует услуги Google OAuth2, чтобы предоставить вам возможность войти в свою учетную запись через свой профиль Google."
              " Мы храним ваши данные так же, как и при обычной регистрации. Безопасность ваших данных, поступающих из Google, контролируется самим Google. У нас нет доступа к вашим данным, которые находятся в Google."
              " Вы можете узнать больше о том, как Google хранит ваши данные на следующей странице: https://policies.google.com/privacy",
        "en": "uses the services of Google OAuth2 to provide you with the opportunity to log in to your account via your Google profile."
              " We store your data in the same way as with normal registration. The security of your data coming from Google is controlled by Google. We do not have access to your data that are in Google."
              " You can read more about how Google stores your data on the following page: https://policies.google.com/privacy"
    },
    "privacypolicytext10": {
        "bg": " използва cookies (бисквитки), за да ви предостави използването на сайта. Без тях, сайтът няма да работи правилно."
               " Ако вашите бисквитки са изключени, няма да можете да използвате сайта. Информацията, събирана от бисквитките съдържа вашият уникален идентификатор, вашият предпочитан език и други данни, които са необходими за сайта да работи."
               " Можете да прочетете повече за това как работят бисквитките на следната страница: https://www.aboutcookies.org/",
        "es": " utiliza cookies para que pueda utilizar el sitio web. Sin ellas, el sitio web no funcionará correctamente."
                " Si tiene las cookies deshabilitadas, no podrá utilizar el sitio web. La información recopilada por las cookies contiene su identificador único, su idioma preferido y otros datos necesarios para que el sitio web funcione."
                " Puede leer más sobre cómo funcionan las cookies en la siguiente página: https://www.aboutcookies.org/",
        "de": " verwendet Cookies, damit Sie die Website nutzen können. Ohne sie funktioniert die Website nicht richtig."
                " Wenn Sie die Cookies deaktiviert haben, können Sie die Website nicht nutzen. Die von den Cookies gesammelten Informationen enthalten Ihre eindeutige Kennung, Ihre bevorzugte Sprache und andere Daten, die für die ordnungsgemäße Funktion der Website erforderlich sind."
                " Sie können mehr darüber lesen, wie Cookies funktionieren, auf der folgenden Seite: https://www.aboutcookies.org/",
        "fr": " utilise des cookies pour vous permettre d'utiliser le site Web. Sans eux, le site Web ne fonctionnera pas correctement."
                " Si vous avez désactivé les cookies, vous ne pourrez pas utiliser le site Web. Les informations recueillies par les cookies contiennent votre identifiant unique, votre langue préférée et d'autres données nécessaires au bon fonctionnement du site Web."
                " Vous pouvez en savoir plus sur le fonctionnement des cookies sur la page suivante: https://www.aboutcookies.org/",
        "ru": " использует cookies (куки), чтобы вы могли использовать веб-сайт. Без них веб-сайт не будет работать правильно."
                " Если ваши куки отключены, вы не сможете использовать веб-сайт. Информация, собираемая куками, содержит ваш уникальный идентификатор, ваш предпочитаемый язык и другие данные, необходимые для работы веб-сайта."
                " Вы можете узнать больше о том, как работают куки на следующей странице: https://www.aboutcookies.org/",
        "en": " uses cookies to allow you to use the website. Without them, the website will not work correctly."
                " If you have disabled cookies, you will not be able to use the website. The information collected by the cookies contains your unique identifier, your preferred language and other data necessary for the website to work."
                " You can read more about how cookies work on the following page: https://www.aboutcookies.org/",
    },
    "privacypolicytext11": {
        "bg": " съхранява вашата чувствителна информация, като например вашите пароли, в защитени бази данни. Никой няма достъп до вашата чувствителна информация, освен администраторите на сайта."
              " Тя се съхранява под формата на хеширани пароли, които не могат да бъдат декодирани. Всички пароли са хеширани с SHA-256 алгоритъм."
              " Това осигурява, че вашата парола ще бъде много трудна за прочитане, дори ако някой се опита да я декодира.",
        "es": " guarda su información sensible, como sus contraseñas, en bases de datos protegidas. Nadie tiene acceso a su información sensible, excepto los administradores del sitio."
                " Se almacena en forma de contraseñas cifradas que no se pueden descifrar. Todas las contraseñas están saladas y cifradas con el algoritmo SHA-256."
                " Esto garantiza que su contraseña será muy difícil de leer, incluso si alguien intenta descifrarla.",
        "de": " speichert Ihre sensible Information, wie z. B. Ihr Passwort, in geschützten Datenbanken. Niemand hat Zugriff auf Ihre sensible Information, außer den Administratoren der Website."
                " Es wird in Form von verschlüsselten Passwörtern gespeichert, die nicht entschlüsselt werden können. Alle Passwörter sind gesalzen und verschlüsselt mit dem SHA-256-Algorithmus."
                " Dies garantiert, dass Ihr Passwort sehr schwer zu lesen ist, selbst wenn jemand versucht, es zu entschlüsseln.",
        "fr": " stocke vos informations sensibles, telles que vos mots de passe, dans des bases de données protégées. Personne n'a accès à vos informations sensibles, à l'exception des administrateurs du site."
                " Il est stocké sous forme de mots de passe chiffrés qui ne peuvent pas être déchiffrés. Tous les mots de passe sont salés et chiffrés avec l'algorithme SHA-256."
                " Cela garantit que votre mot de passe sera très difficile à lire, même si quelqu'un essaie de le déchiffrer.",
        "en": " stores your sensitive information, such as your passwords, in protected databases. No one has access to your sensitive information, except the site administrators."
                " It is stored in the form of encrypted passwords that cannot be decrypted. All passwords are encrypted with the SHA-256 algorithm."
                " This ensures that your password will be very difficult to read, even if someone tries to decrypt it.",
        "ru": " хранит вашу чувствительную информацию, такую как ваши пароли, в защищенных базах данных. Никто не имеет доступа к вашей чувствительной информации, кроме администраторов сайта."
                " Он хранится в виде зашифрованных паролей, которые не могут быть расшифрованы. Все пароли зашифрованы алгоритмом SHA-256."
                " Это гарантирует, что ваш пароль будет очень трудно прочитать, даже если кто-то попытается его расшифровать.",
    },
    "privacypolicytext12": {
        "bg": " използва Google Analytics, за да събира информация за вашето поведение на сайта. "
              " Това включва вашият IP адрес, браузър, операционна система, страници, които посещавате и времето, проведено на сайта."
              " Освен това, Google Analytics събира информация за страната или региона, от който сте, както и за вашето местоположение. "
              " Имайте предвид, че тези данни са анонимни и не могат да бъдат използвани за идентификация на конкретни лица. "
              " Данните тип 'локация' са приблизителни и не предоставят точното местонахождение на потребителя, а в регион от няколко километра.",
        "de": " verwendet Google Analytics, um Informationen über Ihr Verhalten auf der Website zu sammeln."
                " Dies umfasst Ihre IP-Adresse, Ihren Browser, Ihr Betriebssystem, die von Ihnen besuchten Seiten und die Zeit, die Sie auf der Website verbracht haben."
                " Darüber hinaus sammelt Google Analytics Informationen über das Land oder die Region, aus der Sie kommen, sowie über Ihren Standort."
                " Beachten Sie, dass diese Daten anonym sind und nicht zur Identifizierung bestimmter Personen verwendet werden können."
                " Daten wie 'Standort' sind ungefähr und geben nicht den genauen Standort des Benutzers an, sondern einen Bereich von einigen Kilometern.",
        "en": " uses Google Analytics to collect information about your behavior on the site."
                " This includes your IP address, browser, operating system, pages you visit and the time you spend on the site."
                " In addition, Google Analytics collects information about the country or region from which you come, as well as your location."
                " Keep in mind that these data are anonymous and cannot be used to identify specific individuals."
                " Data like 'location' are approximate and do not give the exact location of the user, but a region of a few kilometers.",
        "ru": " использует Google Analytics для сбора информации о вашем поведении на сайте."
                " Это включает ваш IP-адрес, браузер, операционную систему, страницы, которые вы посещаете, и время, проведенное на сайте."
                " Кроме того, Google Analytics собирает информацию о стране или регионе, из которого вы пришли, а также о вашем местоположении."
                " Имейте в виду, что эти данные анонимны и не могут использоваться для идентификации конкретных лиц."
                " Данные, такие как 'местоположение', приблизительны и не дают точное местоположение пользователя, а регион в нескольких километрах.",
        "fr": " utilise Google Analytics pour collecter des informations sur votre comportement sur le site."
                " Cela comprend votre adresse IP, votre navigateur, votre système d'exploitation, les pages que vous visitez et le temps que vous passez sur le site."
                " En outre, Google Analytics collecte des informations sur le pays ou la région d'où vous venez, ainsi que votre emplacement."
                " Gardez à l'esprit que ces données sont anonymes et ne peuvent pas être utilisées pour identifier des personnes spécifiques."
                " Les données comme 'emplacement' sont approximatives et ne donnent pas l'emplacement exact de l'utilisateur, mais une région de quelques kilomètres.",
        "es": " utiliza Google Analytics para recopilar información sobre su comportamiento en el sitio."
                " Esto incluye su dirección IP, su navegador, su sistema operativo, las páginas que visita y el tiempo que pasa en el sitio."
                " Además, Google Analytics recopila información sobre el país o región desde el que proviene, así como su ubicación."
                " Tenga en cuenta que estos datos son anónimos y no se pueden utilizar para identificar a personas específicas."
                " Los datos como 'ubicación' son aproximados y no dan la ubicación exacta del usuario, sino una región de unos pocos kilómetros.",

    },
    "privacypolicytext13": {
        "bg": " не упражнява контрол над качваните от потребителите файлове (потребителско-генерирано съдържание) и не носи отговорност за тях и за съдържанието, което те съдържат."
              " Имайте предвид, че тези файлове могат да съдържат информация, която е лична за вас, като например вашите имена, адреси, телефонни номера, фотографии, видео, аудио и други."
              " Файловете са защитени, но не са криптирани и не са защитени от парола. Ние не можем да гарантираме, че някой друг не може да получи достъп до тези файлове в случай, че сървърът бъде хакнат."
              " Препоръчваме да използвате алтернативни методи за съхранение на лична информация, като например криптиране на файловете, преди да ги качите на сайта.",
        "en": " does not control the files uploaded by users (user-generated content) and is not responsible for them and for the content they contain."
                "Keep in mind that these files may contain information that is personal to you, such as your names, addresses, phone numbers, photos, videos, audio and other."
                "The files are protected, but not encrypted and not password protected. We cannot guarantee that someone else cannot access these files in case the server is hacked."
                "We recommend using alternative methods for storing personal information, such as encrypting the files before uploading them to the site.",
        "de": " hat keinen Einfluss auf die von Benutzern hochgeladenen Dateien (benutzergeneriertes Material) und ist nicht für sie und den Inhalt verantwortlich, den sie enthalten."
                "Beachten Sie, dass diese Dateien persönliche Informationen enthalten können, wie z. B. Ihre Namen, Adressen, Telefonnummern, Fotos, Videos, Audio und andere."
                "Die Dateien sind geschützt, aber nicht verschlüsselt und nicht mit einem Passwort geschützt. Wir können nicht garantieren, dass jemand anders in diesem Fall nicht auf diese Dateien zugreifen kann, wenn der Server gehackt wird."
                "Wir empfehlen die Verwendung alternativer Methoden zur Speicherung persönlicher Informationen, wie z. B. das Verschlüsseln der Dateien, bevor Sie sie auf die Website hochladen.",
        "fr": " n'exerce aucun contrôle sur les fichiers téléchargés par les utilisateurs (contenu généré par l'utilisateur) et n'est pas responsable de ceux-ci et du contenu qu'ils contiennent."
                "Gardez à l'esprit que ces fichiers peuvent contenir des informations personnelles, telles que vos noms, adresses, numéros de téléphone, photos, vidéos, audio et autres."
                "Les fichiers sont protégés, mais non cryptés et non protégés par mot de passe. Nous ne pouvons pas garantir qu'une autre personne ne peut pas accéder à ces fichiers en cas de piratage du serveur."
                "Nous vous recommandons d'utiliser des méthodes alternatives pour stocker des informations personnelles, telles que le cryptage des fichiers avant de les télécharger sur le site.",
        "ru": " не контролирует загруженные пользователем файлы (пользовательское сгенерированное содержимое) и не несет ответственности за них и за содержимое, которое они содержат."
                "Имейте в виду, что эти файлы могут содержать личную информацию, такую как ваши имена, адреса, номера телефонов, фотографии, видео, аудио и другие."
                "Файлы защищены, но не зашифрованы и не защищены паролем. Мы не можем гарантировать, что кто-то другой не может получить доступ к этим файлам в случае взлома сервера."
                "Мы рекомендуем использовать альтернативные методы для хранения личной информации, такие как шифрование файлов перед их загрузкой на сайт.",
        "es": " no controla los archivos cargados por los usuarios (contenido generado por el usuario) y no es responsable de ellos ni del contenido que contienen."
                "Ten en cuenta que estos archivos pueden contener información personal, como tus nombres, direcciones, números de teléfono, fotos, videos, audio y otros."
                "Los archivos están protegidos, pero no están cifrados ni protegidos con contraseña. No podemos garantizar que otra persona no pueda acceder a estos archivos en caso de que el servidor sea pirateado."
                "Recomendamos usar métodos alternativos para almacenar información personal, como cifrar los archivos antes de cargarlos al sitio.",


    },
    "activatetext": {
        "bg": "Активиране на служител",
        "es": "Activar empleado",
        "de": "Mitarbeiter aktivieren",
        "fr": "Activer l'employé",
        "ru": "Активировать сотрудника",
        "en": "Activate employee"
    },
    "activatetext1": {
        "bg": "Вие сте на път да активирате служител с ID: ",
        "es": "Estás a punto de activar al empleado con ID: ",
        "de": "Sie sind dabei, den Mitarbeiter mit der ID: zu aktivieren",
        "fr": "Vous êtes sur le point d'activer l'employé avec l'ID: ",
        "ru": "Вы собираетесь активировать сотрудника с ID: ",
        "en": "You are about to activate the employee with ID: "
    },
    "makesuretext1": {
        "bg": "Бъдете сигурни, че активирате правилният човек!!",
        "es": "¡Asegúrate de activar la persona correcta!",
        "de": "Stellen Sie sicher, dass Sie die richtige Person aktivieren!",
        "fr": "Assurez-vous d'activer la bonne personne!",
        "ru": "Убедитесь, что вы активируете правильного человека!",
        "en": "Make sure you activate the right person!",
    },
    "areyousure": {
        "bg": "Сигурни ли сте?",
        "es": "¿Estás seguro?",
        "de": "Bist du sicher?",
        "fr": "Es-tu sûr?",
        "ru": "Ты уверен?",
        "en": "Are you sure?"
    },
    "welcome": {
        "bg": "Добре дошъл/дошла",
        "es": "Bienvenido",
        "de": "Willkommen",
        "fr": "Bienvenue",
        "ru": "Добро пожаловать",
        "en": "Welcome"
    },
    "sorttext": {
        "bg": "Сортиране",
        "es": "Clasificación",
        "de": "Sortierung",
        "fr": "Trier",
        "ru": "Сортировка",
        "en": "Sorting"
    },
    "sortnametext": {
        "bg": "По Име",
        "es": "Por nombre",
        "de": "Nach Name",
        "fr": "Par nom",
        "ru": "По имени",
        "en": "By Name"
    },
    "sortemailtext": {
        "bg": "По Имейл",
        "es": "Por correo electrónico",
        "de": "Nach E-Mail",
        "fr": "Par courriel",
        "ru": "По электронной почте",
        "en": "By Email"
    },
    "sorttaskstext": {
        "bg": "По Незавършени Задачи",
        "es": "Por tareas pendientes",
        "de": "Nach offenen Aufgaben",
        "fr": "Par tâches en attente",
        "ru": "По незавершенным задачам",
        "en": "By Pending Tasks"
    },
    "currentlysorting": {
        "bg": "Текущо сортиране: ",
        "es": "Clasificación actual: ",
        "de": "Aktuelle Sortierung: ",
        "fr": "Tri actuel: ",
        "ru": "Текущая сортировка: ",
        "en": "Current sorting: "
    },
    "nonetext": {
        "bg": "Няма",
        "es": "Ninguno",
        "de": "Keine",
        "fr": "Aucun",
        "ru": "Нет",
        "en": "None"
    },
    "unarchive": {
        "bg": "Въстановяване",
        "es": "Desarchivar",
        "de": "Wiederherstellen",
        "fr": "Désarchiver",
        "ru": "Восстановление",
        "en": "Unarchive"
    },
    "fullydelete": {
        "bg": "Пълно изтриване",
        "es": "Eliminar completamente",
        "de": "Vollständiges Löschen",
        "fr": "Supprimer complètement",
        "ru": "Полное удаление",
        "en": "Fully delete"
    },
    "search": {
        "bg": "Търсене",
        "es": "Buscar",
        "de": "Suche",
        "fr": "Chercher",
        "ru": "Поиск",
        "en": "Search"
    },
    "loginwith": {
        "en": "LOGIN WITH",
        "bg": "ВХОД С",
        "es": "INICIAR SESIÓN CON",
        "de": "ANMELDEN MIT",
        "fr": "SE CONNECTER AVEC",
        "ru": "ВОЙТИ С"
    },
    "signupwith": {
        "en": "SIGN UP WITH",
        "bg": "РЕГИСТРАЦИЯ С",
        "es": "REGÍSTRATE CON",
        "de": "REGISTRIEREN MIT",
        "fr": "S'INSCRIRE AVEC",
        "ru": "ЗАРЕГИСТРИРОВАТЬСЯ С"
    },
    "desctext": {
        "bg": "Описание",
        "es": "Descripción",
        "de": "Beschreibung",
        "fr": "La description",
        "ru": "Описание",
        "en": "Description"
    },
    "invalidname": {
        "bg": "Невалидно име",
        "es": "Nombre inválido",
        "de": "Ungültiger Name",
        "fr": "Nom invalide",
        "ru": "Неверное имя",
        "en": "Invalid name"
    },
    "invalidemail": {
        "bg": "Невалиден имейл",
        "es": "Correo electrónico inválido",
        "de": "Ungültige E-Mail",
        "fr": "Email invalide",
        "ru": "Неверный адрес электронной почты",
        "en": "Invalid email"
    },
    "invalidmessage": {
        "bg": "Невалидно съобщение",
        "es": "Mensaje inválido",
        "de": "Ungültige Nachricht",
        "fr": "Message invalide",
        "ru": "Неверное сообщение",
        "en": "Invalid message"
    },
    "emailsent": {
        "bg": "Съобщението е изпратено",
        "es": "El mensaje se ha enviado",
        "de": "Die Nachricht wurde gesendet",
        "fr": "Le message a été envoyé",
        "ru": "Сообщение отправлено",
        "en": "Message sent"
    },
    "message": {
        "bg": "Съобщение",
        "es": "Mensaje",
        "de": "Nachricht",
        "fr": "Message",
        "ru": "Сообщение",
        "en": "Message"
    },
    "chatnav": {
        "bg": "Чат",
        "es": "Chat",
        "de": "Chat",
        "fr": "Chat",
        "ru": "Чат",
        "en": "Chat"
    },
    "uploadfilebtn": {
        "bg": "Качи файл",
        "es": "Subir archivo",
        "de": "Datei hochladen",
        "fr": "Télécharger un fichier",
        "ru": "Загрузить файл",
        "en": "Upload file"
    },
    "comment": {
        "bg": "Коментар",
        "es": "Comentario",
        "de": "Kommentar",
        "fr": "Commentaire",
        "ru": "Комментарий",
        "en": "Comment"
    },
    "sorttypestatus": {
        "bg": "Статус",
        "es": "Estado",
        "de": "Status",
        "fr": "Statut",
        "ru": "Статус",
        "en": "Status"
    },
    "sorttypedate": {
        "bg": "Дата",
        "es": "Fecha",
        "de": "Datum",
        "fr": "Date",
        "ru": "Дата",
        "en": "Date"
    },
    "sorttypetitle": {
        "bg": "Заглавие",
        "es": "Título",
        "de": "Titel",
        "fr": "Titre",
        "ru": "Заголовок",
        "en": "Title"
    },
    "sorttypearchive": {
        "bg": "Архив",
        "es": "Archivo",
        "de": "Archiv",
        "fr": "Archive",
        "ru": "Архив",
        "en": "Archive"
    },
    "filealreadyattached": {
        "bg": "Файлът е прикачен",
        "es": "El archivo ya está adjunto",
        "de": "Die Datei ist bereits angehängt",
        "fr": "Le fichier est déjà attaché",
        "ru": "Файл уже прикреплен",
        "en": "File already attached"
    },
    "fileuploadtext": {
        "bg": "Качете файл",
        "es": "Subir archivo",
        "de": "Datei hochladen",
        "fr": "Télécharger un fichier",
        "ru": "Загрузить файл",
        "en": "Upload file"
    },
    "changeprofilepicture": {
        "bg": "Смени профилна снимка",
        "es": "Cambiar foto de perfil",
        "de": "Profilbild ändern",
        "fr": "Changer la photo de profil",
        "ru": "Сменить фото профиля",
        "en": "Change profile picture"
    },
    "signinwithgithub": {
        "bg": "Влез с GitHub",
        "es": "Iniciar sesión con GitHub",
        "de": "Mit GitHub anmelden",
        "fr": "Se connecter avec GitHub",
        "ru": "Войти с помощью GitHub",
        "en": "Sign in with GitHub"
    },
    "signinwithfacebook": {
        "bg": "Влез с Facebook",
        "es": "Iniciar sesión con Facebook",
        "de": "Mit Facebook anmelden",
        "fr": "Se connecter avec Facebook",
        "ru": "Войти с помощью Facebook",
        "en": "Sign in with Facebook"
    },
    "youareloggedinas": {
        "bg": "Вие сте влезли като",
        "es": "Has iniciado sesión como",
        "de": "Sie sind angemeldet als",
        "fr": "Vous êtes connecté en tant que",
        "ru": "Вы вошли как",
        "en": "You are logged in as"
    },
    "employee": {
        "bg": "Служител",
        "es": "Empleado",
        "de": "Mitarbeiter",
        "fr": "Employé",
        "ru": "Сотрудник",
        "en": "Employee"
    },
    "welcometotasklify": {
        "bg": "Добре дошли в Tasklify",
        "es": "Bienvenido a Tasklify",
        "de": "Willkommen bei Tasklify",
        "fr": "Bienvenue sur Tasklify",
        "ru": "Добро пожаловать в Tasklify",
        "en": "Welcome to Tasklify"
    },
    "getstartednow": {
        "bg": "Започнете сега!",
        "es": "Empezar ahora!",
        "de": "Jetzt starten!",
        "fr": "Commencer maintenant!",
        "ru": "Начать сейчас!",
        "en": "Get started now!"
    },
    "maketaskalloc": {
        "en": "MAKE TASK ALLOCATION",
        "bg": "НАПРАВИ РАЗПРЕДЕЛЕНИЕTO НА ЗАДАЧИ",
        "es": "HACER ASIGNACIÓN DE TAREAS",
        "de": "TASCHENVERTEILUNG MACHEN",
        "fr": "FAIRE UNE ALLOCATION DE TÂCHES",
        "ru": "СДЕЛАТЬ РАСПРЕДЕЛЕНИЕ ЗАДАЧ"
    },
    "enteridofchatpartner": {
        "en": "Enter ID of the person you want to chat with",
        "bg": "Въведете ID на човека, с когото искате да разговаряте",
        "es": "Ingrese la identificación de la persona con la que desea chatear",
        "de": "Geben Sie die ID der Person ein, mit der Sie chatten möchten",
        "fr": "Entrez l'identifiant de la personne avec laquelle vous souhaitez discuter",
        "ru": "Введите идентификатор человека, с которым вы хотите поболтать"
    },
    "idislocatedinprofilepage": {
        "en": "ID is located in the profile page",
        "bg": "ID се намира в страницата с профила",
        "es": "La identificación se encuentra en la página de perfil",
        "de": "Die ID befindet sich auf der Profilseite",
        "fr": "L'identifiant se trouve sur la page de profil",
        "ru": "Идентификатор находится на странице профиля"
    },
    "idisnotvalid": {
        "en": "ID is not valid",
        "bg": "ID не е валиден",
        "es": "La identificación no es válida",
        "de": "Die ID ist nicht gültig",
        "fr": "L'identifiant n'est pas valide",
        "ru": "Идентификатор недействителен"
    },
    "chatcreated": {
        "en": "Chat created",
        "bg": "Чатът е създаден",
        "es": "Chat creado",
        "de": "Chat erstellt",
        "fr": "Chat créé",
        "ru": "Чат создан"
    },
    "otherpersoncanclosethechatatanytime": {
        "en": "The other person can close the chat at any time",
        "bg": "Другия човек може да затвори чата по всяко време",
        "es": "La otra persona puede cerrar el chat en cualquier momento",
        "de": "Die andere Person kann den Chat jederzeit schließen",
        "fr": "L'autre personne peut fermer le chat à tout moment",
        "ru": "Другой человек может закрыть чат в любое время"
    },
    "createchat": {
        "en": "Create chat",
        "bg": "Създай чат",
        "es": "Crear chat",
        "de": "Chat erstellen",
        "fr": "Créer un chat",
        "ru": "Создать чат"
    },
    "inyourorganization": {
        "en": "In your organization",
        "bg": "Във вашата организация",
        "es": "En tu organización",
        "de": "In deinem Unternehmen",
        "fr": "Dans votre organisation",
        "ru": "В вашей организации"
    },
    "enter2fa": {
        "en": "Please enter the 2FA code provided by your authenticator app",
        "bg": "Моля, въведете 2FA кода, предоставен от приложението за удостоверяване",
        "es": "Ingrese el código 2FA proporcionado por su aplicación de autenticación",
        "de": "Bitte geben Sie den 2FA-Code ein, der von Ihrer Authentifizierungs-App bereitgestellt wird",
        "fr": "Veuillez saisir le code 2FA fourni par votre application d'authentification",
        "ru": "Пожалуйста, введите код 2FA, предоставленный вашим приложением для аутентификации"
    },
    "gate2fa": {
        "en": "This account is protected by 2FA",
        "bg": "Този акаунт е защитен с 2FA",
        "es": "Esta cuenta está protegida por 2FA",
        "de": "Dieses Konto ist durch 2FA geschützt",
        "fr": "Ce compte est protégé par 2FA",
        "ru": "Этот аккаунт защищен 2FA"
    },
    "privacypolicytext14": {
        "en": " uses certain Google API services to provide you with a seamless and efficient user experience."
              " We want you to know that we take your privacy seriously, and as such, any information received from Google APIs will be used and transferred in compliance with Google API Services User Data Policy, including the Limited Use requirements."
              " This means that we will only collect and use the data necessary for the specific purposes for which the APIs were authorized and will not use the data for any other purposes without obtaining additional consent from you."
              " By using Tasklify, you consent to our collection, use, and transfer of your information as described in this policy.",
        "bg": " използва определени услуги на Google API, за да ви предостави непрекъснато и ефективно потребителско изживяване."
                "Искаме да ви кажем, че сериозно се занимаваме с вашата поверителност и, като такъв, всички получени от Google API информация ще бъдат използвани и прехвърляни в съответствие с Политиката за данни на потребителите на услугите на Google API, включително изискванията за ограничено използване."
                "Това означава, че ще събираме и използваме само данните, необходими за конкретните цели, за които са упълномощени API-та, и няма да използваме данните за други цели без да получите допълнително съгласие от вас."      
                "Използвайки Tasklify, вие се съгласявате със събирането, използването и прехвърлянето на вашата информация, както е описано в тази политика.",
        "es": " usa ciertos servicios de API de Google para brindarle una experiencia de usuario sin problemas y eficiente."
                "Queremos que sepa que tomamos su privacidad en serio y, por lo tanto, cualquier información recibida de las API de Google se utilizará y transferirá de conformidad con la Política de datos de usuarios de servicios de API de Google, incluidos los requisitos de uso limitado."
                "Esto significa que solo recopilaremos y utilizaremos los datos necesarios para los fines específicos para los que se autorizaron las API y no utilizaremos los datos para ningún otro propósito sin obtener su consentimiento adicional."
                "Al usar Tasklify, usted consiente el uso de su información como se describe en esta política.",
        "de": " verwendet bestimmte Google API-Dienste, um Ihnen eine reibungslose und effiziente Benutzererfahrung zu bieten."
                "Wir möchten, dass Sie wissen, dass wir Ihre Privatsphäre ernst nehmen und daher alle von Google APIs erhaltenen Informationen gemäß der Datenschutzrichtlinie für Google API Services User Data Policy, einschließlich der Anforderungen für eine eingeschränkte Nutzung, verwenden und übertragen."
                "Dies bedeutet, dass wir nur die Daten sammeln und verwenden, die für die spezifischen Zwecke erforderlich sind, für die die APIs autorisiert wurden, und die Daten nicht für andere Zwecke verwenden werden, ohne Ihre zusätzliche Zustimmung einzuholen."
                "Durch die Verwendung von Tasklify stimmen Sie unserer Sammlung, Verwendung und Übertragung Ihrer Informationen gemäß dieser Richtlinie zu.",
        "fr": " utilise certaines API Google pour vous fournir une expérience utilisateur fluide et efficace."
                "Nous voulons que vous sachiez que nous prenons au sérieux votre vie privée et, par conséquent, toutes les informations reçues des API Google seront utilisées et transférées conformément à la politique de données des utilisateurs des services API Google, y compris les exigences d'utilisation limitée."
                "Cela signifie que nous ne collecterons et n'utiliserons que les données nécessaires aux fins spécifiques pour lesquelles les API ont été autorisées et n'utiliserons pas les données à d'autres fins sans obtenir votre consentement supplémentaire."
                "En utilisant Tasklify, vous consentez à notre collecte, utilisation et transfert de vos informations conformément à cette politique.",
        "ru": " использует определенные услуги Google API для обеспечения вам беспрепятственного и эффективного пользовательского опыта."
                "Мы хотим, чтобы вы знали, что мы серьезно относимся к вашей конфиденциальности, и, как следствие, любая информация, полученная от API Google, будет использоваться и передаваться в соответствии с Политикой конфиденциальности пользователей услуг API Google, включая требования ограниченного использования."
                "Это означает, что мы будем собирать и использовать только те данные, которые необходимы для конкретных целей, для которых были авторизованы API, и не будем использовать данные для каких-либо других целей без получения вашего дополнительного согласия."
                "Используя Tasklify, вы соглашаетесь с нашей сбором, использованием и передачей ваших данных в соответствии с этой политикой."


    },
    "dates": {
        "en": "Dates",
        "bg": "Дати",
        "es": "Fechas",
        "de": "Termine",
        "fr": "Dates",
        "ru": "Даты"
    },
    "tasks": {
        "en": "Tasks",
        "bg": "Задачи",
        "es": "Tareas",
        "de": "Aufgaben",
        "fr": "Tâches",
        "ru": "Задачи"
    },
    "taskschedule": {
        "en": "Task Schedule",
        "bg": "Разписание на задачите",
        "es": "Programación de tareas",
        "de": "Aufgabenplan",
        "fr": "Planification des tâches",
        "ru": "Расписание задач"
    },
    "calendar": {
        "en": "Calendar",
        "bg": "Календар",
        "es": "Calendario",
        "de": "Kalender",
        "fr": "Calendrier",
        "ru": "Календарь"
    },
}


def getword(word, target):
    if target not in ["en", "bg", "es", "de", "fr", "ru"]:
        return "Тarget language not supported"
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


def gettheme(request):
    if 'theme' in request.cookies:
        return request.cookies.get('theme')
    else:
        return 'light'

