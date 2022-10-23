#your_app/tasks.py
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
logger = get_task_logger(__name__)

@task(name='send_bcc_task')
def send_bcc_task(subject, message, mylist):
    mail = EmailMessage(subject, message, 'chair@dpp-connect.org', bcc=mylist)
    mail.content_subtype = 'html'
    mail.send()

