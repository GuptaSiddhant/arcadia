#######First draft
# Arcadia: Online Game Store
TODO: Write a project description (What and Why)

## Team
Henri Ahti 57237L      
Siddhant Gupta  721936  
Santeri Volkov  528142 

## Features
We will implement the features defined is project description.  In addition to mandatory requirements we are going 
to implement minimum the following extra features:
- social media sharing
- mobile friendly
  
For each feature, how are we going to implement it?
## Models and Views
TODO: Initial ideas for what kind of Models and Views we will be needing, 
and how they relate to each other
(some schematics?)

## Collaboration (planned working practices)
- we use Telegram for communication and collaboration
- we use Gitlab as code repository
- we meet minimum once per week during the project sprints

Git

1. Clone it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D  

## Process and Time Schedule
TODO: Maybe rough estimates of time needed for each implementation

WEEK 51-52
1. Heroku setup (Santeri)
2. Django basic setup (Henri)
    - one app
    - development configuration with SQLLite
    - production configuration with Postgres
    - required middleware for Authentication etc.
    - check / configure default template system used
3. Implement the first models (User(Django), DeveloperProfile, GamerProfile, Transactions, Game, GameState (settings, 
game_state) (Henri)
4. Initial website deign (Siddhant)

WEEK 1 Sprint
- Registration page
- Login page
- Email validation / SMTP sending from Django
- test planning for the project

WEEK 2 Sprint
- DevelopersView
- GamersView
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


