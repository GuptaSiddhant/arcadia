import json

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from app.models import Game, Genre

User = get_user_model()

MAX_JSON_DATA_LEN = 2048


# Modified UserCreationForm to include email, profile image url, and developer registration fields
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True, help_text="A confirmation mail will be sent to this email address.")
    image = forms.URLField(required=False, label='Profile Picture URL',
                           help_text="The image url should begin with \"https://\". [Optional]",
                           validators=[URLValidator(schemes=['https'])])
    dev_registration = forms.BooleanField(required=False, label='Register as Developer',
                                          help_text='Yes, I want to register as a Developer. Being a developer allows '
                                                    'you to submit games to Arcadia.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'image',
                  'dev_registration')

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


# Modified UserChangeForm to include extra fields
class UpdateProfile(UserChangeForm):
    password = None
    image = forms.URLField(required=False, label='Profile Picture URL', help_text="[Optional]",
                           validators=[URLValidator(schemes=['https'])])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'is_dev')
        labels = {'is_dev': 'Act as Developer', }
        help_texts = {
            'image': 'The image url should begin with "https://".',
            'is_dev': 'Tick the box to become a developer.'}


# Form for adding games to the site, to be sold and played
class GameForm(forms.ModelForm):
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=True)

    class Meta:
        model = Game
        fields = ('name', 'genre', 'url', 'description', 'price', 'image')
        labels = {'url': 'Game URL', 'price': 'Cost (€)', 'image': 'Thumbnail Image URL', }
        help_texts = {
            'url': 'Add the link the javascript game (hosted elsewhere). The game url should begin with "https://".',
            'description': 'Few words about game to entice player to purchase.',
            'price': 'Leave it 0 and offer the game as Free to Play.',
            'image': 'Preferred square image with width >= 500px. The image url should begin with "https://". '
                     '[Optional]', }


class MessageForm(forms.Form):
    # Every message should conform to this basic form. We use it as a base class for all
    # the other forms about messaging
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


class MessageLoadForm(MessageForm):

    def clean_messageType(self):
        if self.cleaned_data['messageType'] != 'LOAD_REQUEST':
            raise ValidationError("MessageSaveForm should be created by a LOAD_REQUEST message type.")

        return self.cleaned_data['messageType']
