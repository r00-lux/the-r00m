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

# Setup a venv to prevent conflicts with the base image.
RUN python -m venv /py

# Update pip
RUN /py/bin/pip install --upgrade pip

# # Install Postgres requirements and temporary build requirements.
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps build-base \
    postgresql-dev musl-dev

# Install Python dependencies.
RUN /py/bin/pip install -r /tmp/requirements.txt

# Cleanup temp directory. These files are not needed after installation.
RUN rm -rf /tmp

# Uninstall the temporary build deps.
RUN apk del .tmp-build-deps

# Setup a new user.
RUN adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user