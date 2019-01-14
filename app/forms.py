from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from app.models import Game, Genre, Transaction

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    image = forms.URLField(required=False, label='Profile Picture URL', help_text="[Optional]")
    dev_registration = forms.BooleanField(required=False, label='Register as Developer',
                                          help_text='Yes, I want to register as a Developer. Being a developer allows to submit games to Arcadia.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'image', 'dev_registration')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        user.is_dev = self.cleaned_data['dev_registration']
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
