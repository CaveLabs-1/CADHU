#!/bin/bash
source my_env/bin/activate
cd CADHU
git pull origin develop
pip install -r requirements.txt
for linea in `cat apps.txt`
do
  python manage.py makemigrations $linea
  python manage.py migrate
done
systemctl restart gunicorn
