import os

from dotenv import load_dotenv
import datetime
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(".env")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

mysqlurl = f'mysql://doadmin:{os.getenv("SQL_PASSWORD")}@{os.getenv("SQL_HOST")}:25060/defaultdb'


def sendemail(emailaddr, name, taskcount):
    import os
    import smtplib
    from email.message import EmailMessage
    EMAIL_ADDRESS = "hello@tasklify.me"
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    msg = EmailMessage()
    msg['Subject'] = 'Task Reminder | Напомняне за задачи'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = emailaddr
    msg.set_content('Task Reminder | Напомняне за задачи')
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
                  <h1 style="color:rgb(0, 0, 0); font-family: sans-serif;">Hello, {name}!</h1>
                  <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">You have {taskcount} tasks that are due in the next 24 hours.</h2>
                  <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Please complete them as soon as possible and if you already did - please ignore this email.</h2>
                  <br><br>
                  <hr style="text-align:left;margin-left:0">
                  <br><br>
                  <h1 style="color:rgb(0, 0, 0); font-family: sans-serif;">Здравейте, {name}!</h1>
                  <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Напомняме Ви, че имате {taskcount} незавършени задачи с краен срок след по-малко от 24 часа.</h2>
                  <h2 style="color:rgb(0, 0, 0); font-family: sans-serif;">Моля, завършете ги възможно най-скоро, а ако вече сте - може да игнорирате този Имейл.</h2>
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


def prepareemail(workerlist):
    mydb = mysql.connector.connect(host=os.getenv("SQL_HOST"), user="doadmin", password=os.getenv("SQL_PASSWORD"),
                                   database="defaultdb", port=25060)
    for worker in workerlist:
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM worker WHERE id = '{str(worker)}'")
        myresult = mycursor.fetchall()
        for x in myresult:
            email = x[1]
            name = x[3]
            taskcount = workerlist[worker]
            sendemail(email, name, taskcount)


def checkduedate():

    load_dotenv(".env")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    mydb = mysql.connector.connect(host=os.getenv("SQL_HOST"), user="doadmin", password=os.getenv("SQL_PASSWORD"),
                                   database="defaultdb", port=25060)

    workerlist = {}

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM task")
    myresult = mycursor.fetchall()
    for x in myresult:
        if str(x[4]).split("-")[0] == "DEMO":
            continue
        if x[9] - datetime.datetime.now() < datetime.timedelta(hours=24):
            if x[11] == 0 or x[11] is False:
                mycursor.execute(f"UPDATE task SET notified = 1 WHERE id = {x[0]}")
                mydb.commit()
                if x[4] in workerlist:
                    workerlist[x[4]] += 1
                else:
                    workerlist[x[4]] = 1

    # if worker starts with DEMO, remove it
    if len(workerlist) > 0:
        print(f"Sending emails to {len(workerlist)} workers")
        prepareemail(workerlist)
    else:
        print("No workers to send emails to.")


if __name__ == "__main__":
    checkduedate()
