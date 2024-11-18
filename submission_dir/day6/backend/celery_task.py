from app import celery_app
from celery_context import appContext

celery_app.Task = appContext
@celery_app.task(base=appContext)
def helloWorld():
    from time import sleep
    sleep(10)
    print('Hello, World! from celery task')
    return 'Hello, World!'

@celery_app.task(base=appContext)
def add(a, b):
    return a + b


@celery_app.task()
def retrieve_data(id):
    from models import Category
    data = Category.query.filter_by(id=id).first()
    print(data.name)
    return {'id': data.id, 'name': data.name, 'description': data.description, 'status': data.status, 'created_by': data.created_by}

@celery_app.task()
def send_mail_to_all_users():
    from mailer import mailer
    from models import User
    users = User.query.all()
    for user in users:
        if user.roles[0].name != 'admin':
            from flask_mail import Message
            email_recipient = user.email
            email_subject = 'Test Email'
            email_body = 'This is a test email'
            email_html = "<html><body><h1>This is a test email</h1>"
            email_html += f"<p>Hi, {user.email}<p>"
            email_html += f"<p>{email_body}</p>"
            email_html += f"<p>login count: {user.login_count}</p>"
            email_html += "</body></html>"
            msg = Message(subject=email_subject, recipients=[email_recipient], body=email_body)
            msg.html = email_html
            msg.attach('attachment.txt', 'text/plain', 'This is an attachment')
            mailer.send(msg)
    return 'Mail sent to all users'