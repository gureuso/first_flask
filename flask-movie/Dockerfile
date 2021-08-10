FROM python:3.9
MAINTAINER gureuso <wyun13043@gmail.com>

USER root
WORKDIR /root

# base
RUN apt-get -y update
RUN apt-get -y install python3-pip

# flask
WORKDIR /root/flask-movie
COPY ./ /root/flask-movie
RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt

CMD python manage.py runserver

EXPOSE 80
