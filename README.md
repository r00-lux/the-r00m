# The R00m
The website for The R00m community.

# Dev setup
To setup your local development environment follow these steps.

## ENV
Site settings are pulled from a local .env file. In the root directory of the repo created a file named `.env` and add the following content:
```
DB_USER=devdb
DB_PASS=devdbpass
```
These values can be whatever you want. They are used for setting up the local Postgres database.

## Docker
Navigate to the root directory of the repo. This is where `docker-compose.yml` exists. Build the docker environment with `docker compose build`. Start the site with `docker-compose up -d`.
