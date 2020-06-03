FROM python:3.7
MAINTAINER Raph Gallardo

WORKDIR /discordbot

COPY ./requirements.txt /requirements.txt
COPY ./Dockerfile /Dockerfile

RUN pip install -r /requirements.txt

RUN chmod 755 /discordbot

VOLUME ["/discordbot/"]

CMD ["python", "-u", "/discordbot/pyDiscordBot.py"]
