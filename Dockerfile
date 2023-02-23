FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY . . 

ENTRYPOINT /bin/sh -c bash