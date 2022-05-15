# django-projects
Projects built with Python relying on Django, following along the [Django 3 By Example](https://www.packtpub.com/product/django-3-by-example-third-edition/9781838981952) book written by Antonio Melé.

Running the built-in Django sever over HTTPS
 * choco install mkcert
 * mkcert -cert-file cert.pem -key-file key.pem mysite.com 127.0.0.1
 * python .\manage.py runserver_plus --cert-file .\cert.pem --key-file key.pem

Running Celery
 * choco install rabbitmq
 * rabbitmq-server
 * python -m celery -A myshop worker -l info -P solo
 * python -m celery -A myshop flower