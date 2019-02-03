# Todo
* inventory
    * ext-profile
    * library
    * gameplay
    

## User
* Groups - Admins, Developers, Gamers
* Login

## Profile
* user
* credits
* inventory
* points / level

## Game
* url
* genre
* price
* name
* image (future)
* description
* global-high-score with user

## Transactions
* sales (gameid, playerid, amount, timestamp)

## GameState
* settings
* score
* game_state

## WebViews
* Login/Register
* Browse (no-login)
* Dev-Profile (login-dev)
* Gamer-Profile (login) 
* Details-Purchase-page (no-login) (Highscores)
* Game-Page (login)
* Submit-Game (login-dev)

### Features
* TwitterSharing
* Responsive

#### Commands
source ~/djangoenv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

heroku login
heroku git:remote -a wsd-arcadia
git push heroku master
