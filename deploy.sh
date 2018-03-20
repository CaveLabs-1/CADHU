#!/bin/bash
pip install -r requirements.txt
for linea in `cat apps.txt`
do
  python manage.py makemigrations $linea
  python manage.py migrate
done
sudo systemctl restart gunicorn
deactivate
cd ~
