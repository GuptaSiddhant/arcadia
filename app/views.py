from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from app.models import Developer
from app.models import Player
from app.models import Game
from app.models import Genre


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def Index(request):
    game = Game.objects.get(pk = 1)
    return render(request, 'gameplay/game.html', {'game': game})


def GamePlay(request, game_id):
    try:
        game = Game.objects.get(pk = game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound(request)
    return render(request, 'gameplay/game.html', {'game': game})
