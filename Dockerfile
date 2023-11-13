FROM python:3.4

ADD . .

ENV FLASK_APP run.py

RUN pip3 install -r requirements.txt
#RUN python3 -m venv venv

EXPOSE 5000

CMD . ./venv/bin/activate && FLASK_APP=run.py flask run

WORKDIR /app

COPY . /app