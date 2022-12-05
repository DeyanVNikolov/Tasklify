import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv(".env")
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def sendremainder(emailaddr, accname, taskcount):
    import os
    import smtplib
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

def connect_to_mysql():

    try:
        connection = mysql.connector.connect(host=os.getenv("SQL_HOST"), database="defaultdb", user='doadmin',
                                             password=os.getenv("SQL_PASSWORD"), port=25060)
        if connection.is_connected():
            db_info = connection.get_server_info()

            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None


def get_tasks():
    connection = connect_to_mysql()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM task")
        tasks = cursor.fetchall()
        return tasks
    else:
        return None

def get_worker(id):
    connection = connect_to_mysql()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM worker WHERE id = %s", (id,))
        worker = cursor.fetchone()
        return worker
    else:
        return None


def prepareemail(tasksandworkers, taskcount):

    for taskandworker in tasksandworkers:
        taskandworker = taskandworker.split("  ")

        tasks = taskcount[taskandworker[0]]

        print("Sending email to " + taskandworker[1] + " with " + str(tasks) + " tasks")

        sendremainder(taskandworker[0], taskandworker[1], tasks)



if __name__ == "__main__":
    tasks = get_tasks()
    tasksandworkers = {}
    taskcount = {}
    for task in tasks:
        completed = task[3]
        completed = str(completed)
        if completed != "2":
            workerid = task[4]
            worker = get_worker(workerid)
            emailaddr = worker[1]
            accname = worker[3]
            if emailaddr not in tasksandworkers:
                tasksandworkers[emailaddr+"  "+accname] = 1

            if emailaddr in taskcount:
                taskcount[emailaddr] += 1
            else:
                taskcount[emailaddr] = 1


    prepareemail(tasksandworkers, taskcount)








