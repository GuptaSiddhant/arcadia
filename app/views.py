from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from app.models import User
from app.models import Game
from app.models import Genre


from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from app.forms import SignUpForm


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def game(request):
    return render(request, 'game.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('game')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def Index(request):
    game = Game.objects.get(pk = 1)
    return render(request, 'gameplay/game.html', {'game': game})


def GamePlay(request, game_id):
    try:
        game = Game.objects.get(pk = game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound(request)
    return render(request, 'gameplay/game.html', {'game': game})
