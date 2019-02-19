#### Commands
pip install -r requirements.txt
source ~/djangoenv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

heroku login
heroku git:remote -a arcadiagames
git push heroku master
