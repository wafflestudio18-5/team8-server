#!/bin/bash

source ~/.bash_profile

cd team8-server
git pull origin main

cd podo_server

source activate podo-deploy
pip install -r requirements.txt

python manage.py makemigrations
python manage.py check --deploy

uwsgi --ini /home/ec2-user/team8-server/podo_server/podo_server.ini
sudo nginx -t
sudo service nginx start
