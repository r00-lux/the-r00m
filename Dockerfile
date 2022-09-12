# Base image.
FROM python:3.10.7-alpine3.16

LABEL maintainer="r00"

# Don't buffer Python output to reduce output lag.
ENV PYTHONUNBUFFERED 1

# Copy Python requirments file into the app directory.
COPY requirements.txt /tmp/requirements.txt

# Copy the source code into the app directory.
COPY . /app

# Create and navigate to the app directory.
WORKDIR /app

# Django listens on 8000 by default. Exposing it here maps port 80 
# on the host to 8000 on the container.
EXPOSE 8000

# Setup a venv and install the necessary requirements.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user