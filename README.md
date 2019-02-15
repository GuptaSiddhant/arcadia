# Arcadia: Online Game Store
Arcadia is an online game store for JavaScript games. 
The service has two types of users: players and developers. 
Developers can add their games to the service and set a price for it. 
Players can buy games on the platform and then play purchased games, 
developers can also be players.
 
This is a course project for Web Software Development CS-C3170 2018-2019 at Aalto University

Project online on Heroku:  
http://arcadiagames.ga

## Team
Henri Ahti      57237L  
Siddhant Gupta  721936  
Santeri Volkov  528142  

## Features
We will implement the features defined in the project description.  
In addition to mandatory requirements we are going 
to implement at least the following extra features:
- Social media sharing
- Mobile friendly
- Save/load and resolution  

## Models and Views

### Models
AbstractUser (Django)  
    - username, first_name, last_name, email, password, is_active  

User(AbstractUser)  
    - inventory, points_level, image, is_dev, email_confirmed  

Game  
	- developer, genre, url, price, name, image, description, high_score, is_active  

Genre  
	- name  

Transaction  
	- player, game, amount, timestamp, payment_reference, payment_result  

GameState  
	- player, game, gameState, saveDate  

GameScore  
	- player, game, score, scoreDate  

### Views
Signup  
Login  

Player-Profile (login)  
Dev-Profile (login-dev)  
External-Profile (login)  
Profile-Edit (login)  

Explore (no-login)  
Library (login)  

Game-Details-Purchase-page (no-login)  
Game-Play (login)  
Game-Add (login-dev)  
Game-Edit (login-dev)  
Game-Delete (login-dev)  

![alt text][Model relations]

## Collaboration (planned working practices)
- We use Telegram for communication and collaboration
- We use Gitlab as code repository
- We meet at minimum once per week during the project sprints

Git

1. Clone it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D  

## Process and Time Schedule
WEEK 51-52
1. Heroku setup (Santeri)
2. Django basic setup (Henri)
    - one app
    - development configuration with SQLLite
    - production configuration with Postgres
    - required middleware for Authentication etc.
    - check / configure default template system used
3. Implement the first models (User(Django), DeveloperProfile, 
PlayerProfile, Transactions, Game, GameState (settings, 
game_state) (Henri)
4. Initial website deign (Siddhant)

WEEK 1 Sprint
- Registration page
- Login page
- Email validation / SMTP sending from Django

WEEK 2 Sprint
- test data population (Santeri)
- model diagram update (Santeri)
- revised model implementation & migration (Henri)
- Django Groups into use (Henri)
- GamePlayView (Siddhant)
- ProfileView (Siddhant)
- GameBrowserView (Siddhant)
- message_SCORE(and all other game-service messages) (Siddhant)

WEEK 3 Sprint
- Email validation (Henri)
- payment service integration (Henri)
- Get inventory working (Santeri)
- test data population and some unit tests (Santeri)
- save for GameForm (Santeri)
- save game messages (Santeri)
- ModifyGameView (Siddhant)
- GameDetailView (Siddhant)
- SocialSharing (Siddhant)

WEEK 4 Sprint
- Post message from Template to View (Siddhant)
- Delete Game (Siddhant)
- Update Model-Game (Santeri)
- Settings separation (Santeri)

WEEK 5 Sprint
- Highscores (Game & library) - (Siddhant)
- sales statistics (Siddhant)
- Testing Python files (Henri)
- RestfulAPI (Henri)
- Linting - (Santeri)
- 3rd party Login (Santeri)
- Security (https enforcing and other django settings):  
https://observatory.mozilla.org/analyze/arcadiagames.herokuapp.com

WEEK 6 Sprint
- Testing
- Commenting
- Reporting

WEEK 7 Sprint
- Testing
- Commenting
- Reporting 

Final date 19th of Feb


[Model relations]: app/static/media/arcadia.png "Model relations"
