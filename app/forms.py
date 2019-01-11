from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from app.models import Game
from app.models import Genre

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    dev_registration = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'dev_registration')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        user.is_dev = self.cleaned_data['dev_registration']
        if commit:
            user.save()
        return user


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'genre', 'url', 'description', 'price', 'image')
