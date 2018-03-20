#!/bin/bash
cd /home/mancha/
source my_env/bin/activate
cd CADHU/
pip install -r requirements.txt
git pull origin master
for linea in `cat apps.txt`
do
  python manage.py makemigrations $linea
  python manage.py migrate
done
sudo systemctl restart gunicorn
deactivate
cd ~
