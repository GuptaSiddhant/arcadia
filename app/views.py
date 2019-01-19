from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import login
from app.tokens import account_activation_token
from app.models import User, Game, Genre
from app.forms import GameForm, SignUpForm, UpdateProfile
from project.settings import SECRET_KEY, sid
from hashlib import md5

import logging

logger = logging.getLogger(__name__)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Arcadia Account'
            message = render_to_string('email/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'email/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('profile')
    else:
        return render(request, 'email/account_activation_invalid.html')


def index_view(request):
    red = request.GET.get('redirect', None)
    if red:
        return redirect('/explore/?redirect=' + red)
    else:
        return redirect('/explore/')


def explore_view(request):
    genres = Genre.objects.all()
    genre_tag = request.GET.get('genre', 'all')
    search_tag = request.GET.get('search', None)
    red_tag = request.GET.get('redirect', None)
    page = request.GET.get('page', 1)

    games = Game.objects.all()
    count_g = {'total': games.count,
               'free': games.filter(price=0).count}

    if genre_tag == 'free':
        games = games.filter(price=0)
    elif genre_tag != 'all':
        games = games.filter(genre__name__icontains=genre_tag)

    if search_tag is not None:
        games = games.filter(name__icontains=search_tag)

    # Pagination
    pages = Paginator(games, per_page=10, orphans=0)
    game_list = pages.get_page(page)

    args = {'games': game_list, 'genres': genres, 'count': count_g, 'redirect': red_tag}
    return render(request, 'game/explore.html', args)


def library_view(request):
    genre_tag = request.GET.get('genre', 'all')
    search_tag = request.GET.get('search', None)
    red_tag = request.GET.get('redirect', None)
    page_tag = request.GET.get('page', 1)
    sort_tag = request.GET.get('sort', 'asc')

    games = request.user.inventory.all()

    logger.error(games)
    count = {'total': games.count,
             'free': games.filter(price=0).count}

    genres = {}
    for game in games:
        if game.genre.name in genres:
            genres[game.genre.name] += 1
        else:
            genres[game.genre.name] = 1

    if genre_tag == 'free':
        games = games.filter(price=0)
    elif genre_tag != 'all':
        games = games.filter(genre__name__icontains=genre_tag)

    if search_tag is not None:
        games = games.filter(name__icontains=search_tag)

    if sort_tag == 'desc':
        games = games.order_by('-name')
    elif sort_tag == 'asc':
        games = games.order_by('name')

    # Pagination
    pages = Paginator(games, per_page=10, orphans=0)
    game_list = pages.get_page(page_tag)

    args = {'games': game_list, 'genres': genres, 'count': count, 'redirect': red_tag}
    return render(request, 'profile/library.html', args)


def game_play_view(request, game_id):
    red_tag = request.GET.get('redirect', None)
    try:
        game = Game.objects.get(pk=game_id)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'redirect': red_tag})

    args = {'game': game, 'redirect': red_tag}
    return render(request, 'game/game_play.html', args)


def game_add_view(request):
    red_tag = request.GET.get('redirect', None)
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user
            game.save()
            game.developer.inventory.add(game)
            return redirect('library')
    else:
        form = GameForm()
    return render(request, 'game/game_form.html', {'form': form, 'redirect': red_tag})


def game_edit_view(request, game_id):
    red_tag = request.GET.get('redirect', None)
    if request.method == 'POST':
        game_to_edit = Game.objects.get(pk=game_id)
        form = GameForm(request.POST, instance=game_to_edit)
        form.save()
        return redirect('library')
    else:
        form = GameForm()

        try:
            game = Game.objects.get(pk=game_id)
        except ObjectDoesNotExist:
            return render(request, '404.html')

        if request.user != game.developer:
            return render(request, '403.html', {'redirect': red_tag})

        form.fields['name'].initial = game.name
        form.fields['genre'].initial = game.genre
        form.fields['url'].initial = game.url
        form.fields['description'].initial = game.description
        form.fields['price'].initial = game.price
        form.fields['image'].initial = game.image
        return render(request, 'game/game_form.html', {'form': form, 'game': game, 'redirect': red_tag})



def game_api_latest(request):
    game = Game.objects.latest('pk')
    data = {
        "game": {
            'id': game.id,
            'name': game.name,
            'genre': game.genre.name,
            'url': game.url,
            'price': game.price,
            'image': game.image,
            'desc': game.description,
            'developer': {
                'username': game.developer.username,
                'first_name': game.developer.first_name,
                'last_name': game.developer.last_name,
                'photo': game.developer.image,
            }
        }
    }
    return JsonResponse(data)


def external_profile_view(request, username):
    red_tag = request.GET.get('redirect', None)
    try:
        user2 = User.objects.get(username__contains=username)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'redirect': red_tag})

    games = Game.objects.filter(developer=user2)

    return render(request, 'profile/profile_ext.html', {'user2': user2, 'games': games, 'redirect': red_tag})


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


def pay_purchase_view(request, game_id):
    red_tag = request.GET.get('redirect', None)
    try:
        game = Game.objects.get(pk=game_id)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'redirect': red_tag})

    # Do not know PID yet
    pid = 123
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, game.price, SECRET_KEY)
    checksum = md5(checksumstr.encode("ascii")).hexdigest()

    args = {'game': game, 'redirect': red_tag, 'checksum': checksum, 'sid': sid, 'pid': pid}
    return render(request, 'payment/purchase.html', args)


def payment_result_view(request):
    red_tag = request.GET.get('redirect', None)
    pid_tag = request.GET.get('pid', None)
    reference_tag = request.GET.get('ref', None)
    result_tag = request.GET.get('result', None)
    checksum_tag = request.GET.get('checksum', None)

    valid_transaction = False
    checksumstr = "pid={}&ref={}&result={}&token={}".format(pid_tag, reference_tag, result_tag, SECRET_KEY)
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    if checksum_tag == checksum:
        valid_transaction = True

    # Get Game object from payment id
    try:
        game = Game.objects.get(id=1)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'redirect': red_tag})

    args = {'game': game,
            'redirect': red_tag,
            'reference': reference_tag,
            'result': result_tag,
            'validity': valid_transaction}
    return render(request, 'payment/result.html', args)
