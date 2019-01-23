from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from app.models import Game, Genre, Transaction, GameState, GameScore
from django.core.exceptions import ValidationError
import json

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    image = forms.URLField(required=False, label='Profile Picture URL', help_text="[Optional]")
    dev_registration = forms.BooleanField(required=False, label='Register as Developer',
                                          help_text='Yes, I want to register as a Developer. Being a developer allows you to submit games to Arcadia.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'image', 'dev_registration')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        user.is_dev = self.cleaned_data['dev_registration']
        if self.cleaned_data['image'] == '':
            user.image = 'https://pngimage.net/wp-content/uploads/2018/05/default-user-profile-image-png-2.png'
        if commit:
            user.save()
        return user


class UpdateProfile(UserChangeForm):
    password = None
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'image')


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'genre', 'url', 'description', 'price', 'image')
        labels = {'url': 'Game URL', 'price': 'Cost (€)', 'image': 'Thumbnail Image URL', }
        help_texts = {'url': 'Add the link the javascript game (hosted elsewhere).',
                      'description': 'Few words about game to intice player to purchase.',
                      'price': 'Leave it 0 and offer the game as Free to Play.',
                      'image': '[Optional] Preferred square image with width >= 500px ', }


MAX_JSON_DATA_LEN = 2048


class MessageForm(forms.Form):
    # Every message should conform to this basic form. We use it as a base class for all the other forms about messaging
    messageType = forms.ChoiceField(required=True,
                                    choices=[('SCORE', 'score'), ('SAVE', 'save'), ('LOAD_REQUEST', 'load_request')],
                                    widget=forms.HiddenInput())


class MessageScoreForm(MessageForm):
    score = forms.IntegerField(required=True, widget=forms.HiddenInput())

    def clean_messageType(self):
        if self.cleaned_data['messageType'] != 'SCORE':
            raise ValidationError("MessageScoreForm should be created by a SCORE message type.")
        return self.cleaned_data['messageType']


class MessageSaveForm(MessageForm):
    gameState = forms.CharField(required=True, widget=forms.HiddenInput(), max_length=MAX_JSON_DATA_LEN)

    def clean_messageType(self):
        if self.cleaned_data['messageType'] != 'SAVE':
            raise ValidationError("MessageSaveForm should be created by a SAVE message type.")
        return self.cleaned_data['messageType']

    def clean_gameState(self):
        # Check if the game state is serializable by json and if the length is ok
        try:
            # Check for validity
            tmp = json.loads(self.cleaned_data['gameState'])
        except ValueError:
            raise ValidationError("The game state is not valid json and I refuse to store it.")

        if len(self.cleaned_data['gameState']) > MAX_JSON_DATA_LEN:
            raise ValidationError("The gameState you are trying to save is too large.")

        return self.cleaned_data['gameState']


# Implementing the following class just for consistency. It is not necessary, but I prefer to keep the code linear and
# consistent
class MessageLoadForm(MessageForm):

    def clean_messageType(self):
        if self.cleaned_data['messageType'] != 'LOAD_REQUEST':
            raise ValidationError("MessageSaveForm should be created by a LOAD_REQUEST message type.")

        return self.cleaned_data['messageType']
