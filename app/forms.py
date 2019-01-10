from django import forms
from app.models import Game
from app.models import Genre

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'genre', 'url', 'description', 'price', 'image')
