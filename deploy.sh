#!/bin/bash
for linea in `cat apps.txt`
hola
do
  python manage.py makemigrations $linea
  python manage.py migrate
done
sudo systemctl restart gunicorn
deactivate
cd ~
