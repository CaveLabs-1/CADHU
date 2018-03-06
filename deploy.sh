#!/bin/bash
source my_env/bin/activate
cd CADHU
git pull origin master
pip install -r requirements.txt
for linea in `cat apps.txt`
do
  python manage.py makemigrations $linea
  python manage.py migrate
done
sudo systemctl restart gunicorn
deactivate
cd ~
