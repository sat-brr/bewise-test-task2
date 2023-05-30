FROM python:3.10

WORKDIR /code/
COPY . .

ENV PYTHONBUFFERED=1

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y ffmpeg

RUN pip install --upgrade pip && pip install -r requirements.txt
ENV PYTHONPATH /code/
