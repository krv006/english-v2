redis==5.0.8
django-redis==5.4.0

pip:
	pip freeze > requirements.txt

mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

admin:
	python3 manage.py createsuperuser

celery:
	celery -A root worker -l INFO
