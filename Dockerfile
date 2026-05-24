# syntax=docker/dockerfile:1
FROM python:3.14-slim-trixie

ENV FLASK_APP=app.py

RUN mkdir /app
RUN mkdir /app/lists

WORKDIR /app

RUN apt update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=5s --timeout=5s --start-period=5s \
   CMD curl --fail localhost:5006 || exit 1

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py app.py
COPY todo.py todo.py
COPY static static
COPY templates templates

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=5006"]
