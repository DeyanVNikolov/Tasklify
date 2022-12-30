import os
from dotenv import load_dotenv

load_dotenv(".env")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def sendregisterationemail(emailaddr, accname, regid):
    import os
    import smtplib
    import imghdr
    from email.message import EmailMessage

    EMAIL_ADDRESS = "hello@tasklify.me"
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = 'Registration Successful | Регистрацията е успешна'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = emailaddr

    msg.set_content('Registration Email')

    msg.add_alternative(f"""\
    <!DOCTYPE html>
    <html>
        <body>
            <center>
                <br><br>
                <img style="width: 300px; height: auto;" src="https://cdn.tasklify.me/content-delivery-network/secure/image/default-monochrome-black.png">
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h1 style="color:rgb(0, 0, 0); font-family: sans-serif;">Hello and welcome to Tasklify, {accname}!</h1>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Your email ({emailaddr}) has been registered at <a href="https://tasklify.me">https://tasklify.me</a></h2>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Your registration ID is: {regid}</h2>
                <br><br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">If you did not register at Tasklify, please ignore this email or contact us at <a href="mailto:hq@tasklify.me">hq@tasklify.me</a>
                <br>
                Please note that "hello@tasklify.me" is no-reply and you will not receive an answer from that email.</h2>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h1 style="color:rgb(0, 0, 0); font-family: sans-serif;">Здравейте и добре дошли в TaskLify, {accname}!</h1>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Вашият имейл ({emailaddr}) е регистриран в <a href="https://tasklify.me">https://tasklify.me</a></h2>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Вашият регистрационен номер е: {regid}</h2>
                <br><br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Ако не сте се регистрирали в TaskLify, моля, игнорирайте този имейл или се свържете с нас на <a href="mailto:hq@tasklify.me"><strong>hq@tasklify.me</strong></a>
                <br>
                Моля, обърнете внимание, че <strong>"hello@tasklify.me"</strong> е no-reply и няма да получите отговор от този имейл.</h2>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Best regards,<br>Tasklify Team</h2>
                <br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">С най-добри пожелания,<br>Екипът на Tasklify</h2>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h5>Tasklify, "Studentska" Str. 1, 9000 Varna, Bulgaria <br>
                All rights reserved. © 2022</h5>
                <h5>Available on <a href="https://tasklify.me">https://tasklify.me</a></h5>



            </center>
        </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtppro.zoho.eu', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def sendregisterationemailboss(emailaddr, accname):
    import os
    import smtplib
    import imghdr
    from email.message import EmailMessage

    EMAIL_ADDRESS = "hello@tasklify.me"
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = 'Registration Successful | Регистрацията е успешна'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = emailaddr

    msg.set_content('Registration Email')

    msg.add_alternative(f"""\
    <!DOCTYPE html>
    <html>
        <body>
            <center>
                <br><br>
                <img style="width: 300px; height: auto;" src="https://cdn.tasklify.me/content-delivery-network/secure/image/default-monochrome-black.png">
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h1 style="color:rgb(0, 0, 0); font-family: sans-serif;">Hello and welcome to Tasklify, {accname}!</h1>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Your email ({emailaddr}) has been registered at <a href="https://tasklify.me">https://tasklify.me</a></h2>
                <br><br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">If you did not register at Tasklify, please ignore this email or contact us at <a href="mailto:hq@tasklify.me">hq@tasklify.me</a>
                <br>
                Please note that "hello@tasklify.me" is no-reply and you will not receive an answer from that email.</h2>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h1 style="color:rgb(0, 0, 0); font-family: sans-serif;">Здравейте и добре дошли в TaskLify, {accname}!</h1>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Вашият имейл ({emailaddr}) е регистриран в <a href="https://tasklify.me">https://tasklify.me</a></h2>
                <br><br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Ако не сте се регистрирали в TaskLify, моля, игнорирайте този имейл или се свържете с нас на <a href="mailto:hq@tasklify.me"><strong>hq@tasklify.me</strong></a>
                <br>
                Моля, обърнете внимание, че <strong>"hello@tasklify.me"</strong> е no-reply и няма да получите отговор от този имейл.</h2>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Best regards,<br>Tasklify Team</h2>
                <br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">С най-добри пожелания,<br>Екипът на Tasklify</h2>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h5>Tasklify, "Studentska" Str. 1, 9000 Varna, Bulgaria <br>
                All rights reserved. © 2022</h5>
                <h5>Available on <a href="https://tasklify.me">https://tasklify.me</a></h5>



            </center>
        </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtppro.zoho.eu', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def sendremainder(emailaddr, accname, taskcount):
    import os
    import smtplib
    import imghdr
    from email.message import EmailMessage

    EMAIL_ADDRESS = "hello@tasklify.me"
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = 'Task Reminder | Напомняне за задача'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = emailaddr

    msg.set_content('Task Reminder Email')

    msg.add_alternative(f"""\
    <!DOCTYPE html>
    <html>
        <body>
            <center>
                <br><br>
                <img style="width: 300px; height: auto;" src="https://cdn.tasklify.me/content-delivery-network/secure/image/default-monochrome-black.png">
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h1 style="color:rgb(0, 0, 0); font-family: sans-serif;">{accname}, you have {taskcount} uncompleted tasks!</h1>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Check their progress and due date at: <a href="https://tasklify.me/tasks">https://tasklify.me/tasks</h2>
                <p>This email is sent to {emailaddr} because you have uncompleted tasks. If you have completed them, please ignore this email.</p>
                <p>Thank you for using Tasklify!</p>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h1 style="color:rgb(0, 0, 0); font-family: sans-serif;">{accname}, имате {taskcount} незавършени задачи!</h1>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Проверете напредъка им и крайния срок на: <a href="https://tasklify.me/tasks">https://tasklify.me/tasks</h2>
                <p>Този имейл е изпратен на {emailaddr}, защото имате незавършени задачи. Ако сте ги завършили, моля, игнорирайте този имейл.</p>
                <p>Благодарим ви, че използвате Tasklify!</p>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Best regards,<br>Tasklify Team</h2>
                <br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">С най-добри пожелания,<br>Екипът на Tasklify</h2>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h5>Tasklify, "Studentska" Str. 1, 9000 Varna, Bulgaria <br>
                All rights reserved. © 2022</h5>
                <h5>Available on <a href="https://tasklify.me">https://tasklify.me</a></h5>



            </center>
        </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtppro.zoho.eu', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def sendmail(name, email, message):
    import os
    import smtplib
    import imghdr
    from email.message import EmailMessage

    EMAIL_ADDRESS = "hello@tasklify.me"
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = 'Ново съобщение от ' + name
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ['didonikolovbg@gmail.com', 'anastasov.marti@gmail.com']

    msg.set_content('Tasklify Contact Form')

    msg.add_alternative(f"""\
    <!DOCTYPE html>
    <html>
        <body>
            <center>
                <br><br>
                <img style="width: 300px; height: auto;" src="https://cdn.tasklify.me/content-delivery-network/secure/image/default-monochrome-black.png">
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h1 style="color:rgb(0, 0, 0); font-family: sans-serif;">Ново съобщение от {name},</h1>
                <br><br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">{message}</h2>
                <br><br>
                <br><br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Отговорете на {name} на: <strong>{email}</strong></h2>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Best regards,<br>Tasklify Team</h2>
                <br>
                <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">С най-добри пожелания,<br>Екипът на Tasklify</h2>
                <br><br>
                <hr style="text-align:left;margin-left:0">
                <br><br>
                <h5>Tasklify, "Studentska" Str. 1, 9000 Varna, Bulgaria <br>
                All rights reserved. © 2022</h5>
                <h5>Available on <a href="https://tasklify.me">https://tasklify.me</a></h5>
                
            </center>
        </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtppro.zoho.eu', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
