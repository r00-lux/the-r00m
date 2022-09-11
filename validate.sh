docker compose run --rm app sh -c "flake8"
docker compose run --rm app sh -c "python manage.py test"
