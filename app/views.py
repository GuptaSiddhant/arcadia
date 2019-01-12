from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from app.models import User
from app.models import Game
from app.models import Genre
from app.forms import GameForm
import logging

from app.forms import SignUpForm

logger = logging.getLogger(__name__)


# TODO: automatically log user in maybe after signup?
# from django.contrib.auth import login, authenticate


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    model = User


def ExploreView(request):
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
    return render(request, 'game/explore.html', {'games': games, 'genres': genres})


def GamePlayView(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound(request)
    return render(request, 'game/gameplay.html', {'game': game})


def GameFormView(request):
    form = GameForm()
    return render(request, 'game/form.html', {'form': form})


def LibraryView(request):
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
    return render(request, 'profile/library.html', {'games': games, 'genres': genres})
