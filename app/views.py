from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from app.models import Developer
from app.models import Player
from app.models import Game
from app.models import Genre
import logging

logger = logging.getLogger(__name__)


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def Index(request):
    game = Game.objects.get(pk=1)
    return render(request, 'gameplay/game.html', {'game': game})


def GamePlay(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound(request)
    return render(request, 'gameplay/game.html', {'game': game})


def Explore(request):
    genres = Genre.objects.all()
    genre_tag = request.GET.get('genre', None)
    search_tag = request.GET.get('search', None)

    if search_tag != None:
        games = Game.objects.filter(name__icontains=search_tag)
    else:
        if genre_tag == 'all' or genre_tag == None:
            games = Game.objects.all()
        elif genre_tag == 'free':
            games = Game.objects.filter(price=0)
        else:
            games = Game.objects.filter(genre__name__icontains=genre_tag)
    return render(request, 'explore/explore.html', {'games': games, 'genres': genres})
