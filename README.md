# Arcadia: Online Game Store
TODO: Write a project description (What and Why)

## Team
Henri Ahti 57237L      
Siddhant Gupta  721936  
Santeri Volkov  528142 

## Features
We will implement the features defined in the project description.  In addition to mandatory requirements we are going 
to implement at least the following extra features:
- Social media sharing
- Mobile friendly
- Save/load and resolution 
 
TODO: For each feature, a brief description how do you plan to implement it?
(what is there to say about this? We follow the requirements?) 

## Models and Views
Initial plan of Models and Views we will be implementing, 
and how they relate to each other.

###### Models
* User(Django) -> (Developer, Player)
* Transactions(sales)
* Game
* GameState

###### WebViews
* Login/Register
* Browse (no-login)
* Dev-Profile (login-dev)
* Player-Profile (login) 
* Details-Purchase-page (no-login) (Highscores)
* Game-Page (login)
* Submit-Game (login-dev)

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
3. Implement the first models (User(Django), DeveloperProfile, PlayerProfile, Transactions, Game, GameState (settings, 
game_state) (Henri)
4. Initial website deign (Siddhant)

WEEK 1 Sprint
- Registration page
- Login page
- Email validation / SMTP sending from Django
- test planning for the project

WEEK 2 Sprint
- DevelopersView
- PlayersView
- message_SCORE
- message_SAVE
- message_LOAD
- message_SETTING

WEEK 3 Sprint
- GamePlayView
- SubmitGameView
- message_LOAD_REQUEST
- message_ERROR
- payment service integration

WEEK 4 Sprint
- ModifyGameView
- GameDetailView

WEEK 5 Sprint
- GameBrowserView
- SocialSharing

WEEK 6 Sprint
- Extra features

WEEK 7 Sprint
- Testing

Final date 19th of Feb




[Model relations]: media/Arcadia.png "Model relations"