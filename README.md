
# School Chale Hum 

1. Django app for managing students, their respective schools and books
2. Every student's progress with a particular book can be seen on the app
3. Built Django Command for extracting data from csv and storing it into database
4. Used Heroku Postgres
5. Used REDIS-CLOUD Sever, provided by heroku add-ons
6. Used AWS S3 bucket for static files
7. Used Mail JET API in place of SMTP and used custom reset View to override default send_mail method
8. In built views of PasswordChangeDoneView, PasswordChangeView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetCompleteView, Build Custom Templates for These Inbuilt Views
9. Deployed on Heroku
10. Complete Custom Auth is Implemented

## Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/docs/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
[![Amazon Web Services](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Heroku](https://img.shields.io/badge/-Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://heroku.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Demo

Available at: https://school-chale-hum.herokuapp.com/

admin login details:--
username: admin@arpansahu.me
password: showmecode
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Installation

Installing Pre requisites
```bash
  pip install -r requirements.txt
```

Create .env File and don't forget to add .env to gitignore
```bash
  add variables mentioned in .env.example
```

Making Migrations and Migrating them.
```bash
  python manage.py makemigrations
  python manage.py migrate
```
Run update_data Command
```
  python manage.py update_data
```
Creating Super User
```bash
  python manage.py createsuperuser
```

Installing Redis On Local (For ubuntu) for other Os Please refer to their website https://redis.io/
```bash
  curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
  sudo apt-get update
  sudo apt-get install redis
  sudo systemctl restart redis.service
```
to check if its running or not
```
  sudo systemctl status redis
```
--------------------------

Use these CACHE settings

``` 
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        # 'LOCATION': REDISCLOUD_URL,
        'LOCATION':'redis://localhost:6379'
    }
}
```
---

Run Server
```bash
  python manage.py runserver
```

## Deployment on Heroku

Installing Heroku Cli from : https://devcenter.heroku.com/articles/heroku-cli
Create your account in Heroku.

Inside your project directory

Login Heroku CLI
```bash
  heroku login

```

Create Heroku App

```bash
  heroku create [app_name]

```

Push Heroku App
```
    git push heroku master
```

Configure Heroku App
```bash
  heroku config:set GITHUB_USERNAME=joesmith

```
Configuring Django App for Heroku

Install whitenoise 
```
pip install whitenoise 
```

Include it in Middlewares.
```
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]
```

Create Procfile and include this code snippet in it.
```
release: ./release-tasks.sh
web: gunicorn school_chale_hum.wsgi
```
Create a release-tasks.sh and include this code snippet in it.
```
python manage.py makemigrations
python manage.py migrate
python manage.py update_data                 (optional is you update this csv frequently)
```
Don't forget to make release-tasks.sh file executable using following command
```
chmod +x release-tasks.sh
```
Comment down Database setting and install 

``` 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT'),
#     }
# }
```
```
pip install dj-database-url
```

and add these lines below the commented Database settings
``` 
import dj_database_url
DATABASES = {'default': dj_database_url.config(default=config('DATABASE_URL'))}
```

Change CACHE from 
``` 
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        # 'LOCATION': REDISCLOUD_URL,
        'LOCATION':'redis://localhost:6379'
    }
}
```
to
```
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDISCLOUD_URL,
        #'LOCATION':'redis://localhost:6379'
    }
}
```
## Documentation

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/docs/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
[![Amazon Web Services](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Heroku](https://img.shields.io/badge/-Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://heroku.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

REDIS_URL=

SECRET_KEY=

DEBUG=

ALLOWED_HOSTS=

EMAIL_USER=

EMAIL_PASS=

DATABASE_URL=

MAIL_JET_API_KEY=

MAIL_JET_API_SECRET=

DB_NAME=

DB_USER=

DB_PASSWORD=

DB_HOST=

DB_PORT=

AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_STORAGE_BUCKET_NAME=

DOMAIN=

PROTOCOL=


