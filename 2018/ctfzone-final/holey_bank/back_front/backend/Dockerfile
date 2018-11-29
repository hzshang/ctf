FROM python:3
MAINTAINER a.kolesnikov@bi.zone

ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app

ARG WORKERS=5
ENV WORKERS=${WORKERS}

CMD ["sh", "-c", "./start.sh"]
