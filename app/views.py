from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from app.models import User
from app.models import Game
from app.models import Genre

from app.forms import SignUpForm


# TODO: automatically log user in maybe after signup?
# from django.contrib.auth import login, authenticate


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    model = User


def Index(request):
    game = Game.objects.get(pk = 1)
    return render(request, 'gameplay/game.html', {'game': game})


def GamePlay(request, game_id):
    try:
        game = Game.objects.get(pk = game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound(request)
    return render(request, 'gameplay/game.html', {'game': game})
