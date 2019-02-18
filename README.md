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

#### Authentication / 200
- Henri

#### Basic player functionalities / 300
- Henri (payment)
- Siddhant (games)
- Santeri (users)

#### Basic developer functionalities / 200
- Siddhant
- Santeri

#### Game/service interaction / 200
- Siddhant

#### Quality of Work / 100
- Santeri (quality of code, use of framework)
- Henri (testing)
- Siddhant (UX)

#### Non-functional requirements
- everyone

### Extra features

#### Save/load and resolution feature / 100
- Siddhant

#### 3rd party login / 100
- Santeri

#### RESTful API / 100
- Henri

#### Own game / 100
- Siddhant

#### Mobile Friendly / 50
- Siddhant

#### Social media sharing / 50
- Siddhant


## Models and Views

### Models

##### AbstractUser (Django)
Abstract version of Django's basic User model

	(username, first_name, last_name, email, password, is_active, ...)  

##### User(AbstractUser)  
Modified AbstractUser to include players inventory, experience/loyalty points
and profile image fields as well as developer and email verification boolean fields
into Django's User model

    (inventory, points_level, image, is_dev, email_confirmed)  

##### Game  
Model for website's games. Games are hosted behind developer provided https secured urls

	(developer, genre, url, price, name, image, description, high_score, is_active)  

##### Genre  
Refers to a particular type or style of a game

	(name)  

##### Transaction 
Model for the game purchase transactions to gather data for sales statistics
and to verify users' owned games

	(player, game, amount, timestamp, payment_reference, payment_result)  

##### GameState 
Model for saving the gamestate send by the game and to bind the gamestate
to a player and a game

	(player, game, gameState, saveDate)  

##### GameScore  
Model for saving scores from games, to distinguish the score from the gamestate,
for when only the score is submitted, and also to get access to the global
high scores of the games

	(player, game, score, scoreDate)  

### Views
- Signup  
- Login  

##### Profile
- Player-Profile (login)  
- Dev-Profile (login-dev)  
- External-Profile (login)  
- Profile-Edit (login)  

##### Browsing
- Explore (no-login)  
- Library (login)  

##### Game
- Game-Details-Purchase-page (no-login)  
- Game-Play (login)  
- Game-Add (login-dev)  
- Game-Edit (login-dev)  
- Game-Delete (login-dev)  

![alt text][Model relations]


## Working practices
- We used Telegram for communication and collaboration
- We used Gitlab as code repository
- We divided the project into week long sprints and met once a week plan and collaborate


## Process and Time Schedule plan
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
