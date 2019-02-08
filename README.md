# API-for-Simple-music-Service-DRF
Developed a simple music API using Django rest framework(DRF), DRF-JWT for Auth, login &amp; Dockerised the API. 
Currently I've written only for adding and editting Songs, Work in progress to add other functionlaties. 

Access all my Fav Song list using the API on "127.0.0.1:8000/api/v1/songs"
"127.0.0.1:8000/admin" - For Login Page 

# Technology stack - 
Django - a python web framework
Django REST Framework - a flexible toolkit to build web APIs
SQLite - this is a database server


# Running application - Clone and use command 'docker-compose up' if you've docker running on your machine.
    - cd music_service
    - virtualenv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
    - python manage.py makemigrations
    - python manage.py migrate
    - python manage.py runserver
    
