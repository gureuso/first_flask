from time import sleep
from urllib.parse import quote_plus
from celery import Celery

app = Celery('tasks', broker='sqs://{}:{}@'.format('ACCESS_KEY',
                                                   quote_plus('SECRET_KEY')))


@app.task
def hello():
    sleep(1)
    return 'hello world'
