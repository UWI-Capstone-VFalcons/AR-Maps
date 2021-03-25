release: python flask-migrate.py db init
release: python flask-migrate.py db migrate
release: python flask-migrate.py db upgrade --directory migrations
web: gunicorn -w 4 -b "0.0.0.0:$PORT" app:app