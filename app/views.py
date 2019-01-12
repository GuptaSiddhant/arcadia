from django.http import HttpResponse, HttpResponseNotFound,Http404
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
# from django.contrib.auth import authenticate, login


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/signup.html'
    model = User


def IndexView(request):
    red = request.GET.get('redirect', None)
    if red:
        return redirect('/explore/?redirect=' + red)
    else:
        return redirect('/explore/')

def ExploreView(request):
    genres = Genre.objects.all()
    genre_tag = request.GET.get('genre', None)
    search_tag = request.GET.get('search', None)
    red_tag = request.GET.get('redirect', None)

    if search_tag != None:
        games = Game.objects.filter(name__icontains=search_tag)
    else:
        if genre_tag == 'all' or genre_tag == None:
            games = Game.objects.all()
        elif genre_tag == 'free':
            games = Game.objects.filter(price=0)
        else:
            games = Game.objects.filter(genre__name__icontains=genre_tag)
    return render(request, 'game/explore.html', {'games': games, 'genres': genres, 'redirect': red_tag})


def GamePlayView(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound(request)
    return render(request, 'game/gameplay.html', {'game': game})

def GameAddView(request):
    form = GameForm()
    return render(request, 'game/form.html', {'form': form})



def GameEditView(request, game_id):
    form = GameForm()
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return render(request, '404.html')
    if request.user == game.developer:
        form.fields['name'].initial = game.name
        form.fields['genre'].initial = game.genre
        form.fields['url'].initial = game.url
        form.fields['description'].initial = game.description
        form.fields['price'].initial = game.price
        form.fields['image'].initial = game.image
        return render(request, 'game/form.html', {'form': form, 'game': game})
    else:
        return render(request, '403.html')


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
