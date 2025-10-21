FROM python:3-alpine

RUN apk update

# Required to install cffi
RUN apk add --no-cache gcc musl-dev libffi-dev libressl-dev

RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir --upgrade setuptools

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY mytube/ /app/mytube
COPY migrations/ /app/migrations
COPY run.py /app/

RUN chown -R 1000:1000 /app
USER 1000

CMD gunicorn --workers=1 --threads=1 --forwarded-allow-ips=* --bind=0.0.0.0:5000 --log-level=info run:app