FROM python:3.7.7-slim-buster

RUN apt-get update
RUN apt-get install gnupg wget systemd -y
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc |  apt-key add -

RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.2 main" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list
RUN apt-get update
RUN apt-get install -y mongodb-org

WORKDIR /python

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY *.py ./
COPY python_libs/ ./python_libs/

VOLUME ["/data/db"]
ENTRYPOINT nohup mongod > /tmp/mongodb.logs & python main.py