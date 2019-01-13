from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
from app.models import User, Game, Genre
from app.forms import GameForm, SignUpForm, UpdateProfile
import logging

logger = logging.getLogger(__name__)


# TODO: Maybe we could automatically log the user in after signup?
# from django.contrib.auth import login, authenticate


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/signup.html'
    model = User


def index_view(request):
    red = request.GET.get('redirect', None)
    if red:
        return redirect('/explore/?redirect=' + red)
    else:
        return redirect('/explore/')


def explore_view(request):
    genres = Genre.objects.all()
    genre_tag = request.GET.get('genre', None)
    search_tag = request.GET.get('search', None)
    red_tag = request.GET.get('redirect', None)
    page = request.GET.get('page', 1)

    if genre_tag == 'all' or genre_tag is None:
        games = Game.objects.all()
    elif genre_tag == 'free':
        games = Game.objects.filter(price=0)
    else:
        games = Game.objects.filter(genre__name__icontains=genre_tag)

    if search_tag is not None:
        games = games.filter(name__icontains=search_tag)

    # Pagination
    pages = Paginator(games, per_page=2, orphans=0)
    game_list = pages.get_page(page)
    return render(request, 'game/explore.html', {'games': game_list, 'genres': genres, 'redirect': red_tag})


def library_view(request):
    genres = Genre.objects.all()
    genre_tag = request.GET.get('genre', None)
    search_tag = request.GET.get('search', None)
    red_tag = request.GET.get('redirect', None)
    page = request.GET.get('page', 1)

    if genre_tag == 'all' or genre_tag is None:
        games = Game.objects.all()
    elif genre_tag == 'free':
        games = Game.objects.filter(price=0)
    else:
        games = Game.objects.filter(genre__name__icontains=genre_tag)

    if search_tag is not None:
        games = games.filter(name__icontains=search_tag)

    # Pagination
    pages = Paginator(games, per_page=2, orphans=0)
    game_list = pages.get_page(page)
    return render(request, 'profile/library.html', {'games': game_list, 'genres': genres, 'redirect': red_tag})


def game_play_view(request, game_id):
    red_tag = request.GET.get('redirect', None)
    try:
        game = Game.objects.get(pk=game_id)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'redirect': red_tag})
    return render(request, 'game/game_play.html', {'game': game, 'redirect': red_tag})


def game_add_view(request):
    red_tag = request.GET.get('redirect', None)
    form = GameForm()
    return render(request, 'game/game_form.html', {'form': form, 'redirect': red_tag})


def game_edit_view(request, game_id):
    red_tag = request.GET.get('redirect', None)
    form = GameForm()
    try:
        game = Game.objects.get(pk=game_id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    if request.user == game.developer:
        form.fields['name'].initial = game.name
        form.fields['genre'].initial = game.genre
        form.fields['url'].initial = game.url
        form.fields['description'].initial = game.description
        form.fields['price'].initial = game.price
        form.fields['image'].initial = game.image
        return render(request, 'game/game_form.html', {'form': form, 'game': game, 'redirect': red_tag})
    else:
        return render(request, '403.html', {'redirect': red_tag})


def external_profile_view(request, username):
    red_tag = request.GET.get('redirect', None)
    try:
        user = User.objects.get(username__contains=username)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'redirect': red_tag})
    return render(request, 'profile/profile_ext.html', {'user2': user, 'redirect': red_tag})


def profile_edit_view(request):
    red_tag = request.GET.get('redirect', None)
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form = UpdateProfile(instance=request.user)
        return render(request, 'profile/profile_update.html', {'form': form, 'redirect': red_tag})
