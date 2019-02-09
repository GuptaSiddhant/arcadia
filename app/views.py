import logging
from hashlib import md5

from django.conf import settings
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from app.forms import GameForm, SignUpForm, UpdateProfile
from app.forms import MessageForm, MessageScoreForm, MessageLoadForm, MessageSaveForm
from app.models import User, Game, Genre, Transaction, GameScore, GameState
from app.tokens import account_activation_token

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
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/profile/?redirect=activated')
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

    games = Game.objects.filter(is_active=True)
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

    library_type = request.get_full_path()

    if library_type.__contains__('/dev/'):
        if request.user.is_dev:
            games = Game.objects.filter(developer=request.user, is_active=True)
        else:
            return render(request, '404.html', {'redirect': red_tag})
    else:
        games = request.user.inventory.all()
        games = games.filter(is_active=True)

    logger.error(library_type)
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
        game = Game.objects.get(pk=game_id, is_active=True)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'redirect': red_tag})

    if not request.user.is_anonymous:
        try:
            transaction = Transaction.objects.get(game=game, player=request.user, payment_result='success')
        except ObjectDoesNotExist:
            transaction = 0
    else:
        transaction = 0

    if request.method == 'GET':
        args = {'game': game, 'transaction': transaction, 'redirect': red_tag}
        return render(request, 'game/game_play.html', args)

    elif request.method == 'POST':
        resp = {
            "error": None,
            "result": None
        }

        transaction = None
        try:
            transaction = Transaction.objects.get(game=game, player=request.user, payment_result='success')
        except ObjectDoesNotExist:
            transaction = Transaction.objects.create(game=game,
                                                     player=request.user,
                                                     amount=0,
                                                     payment_reference=0,
                                                     timestamp=timezone.now(),
                                                     payment_result='success')
            request.user.inventory.add(transaction.game)

        form = MessageForm(request.POST)
        if not form.is_valid():
            resp['error'] = form.errors
            return JsonResponse(status=400, data=resp)

        # Specific message:
        if form.cleaned_data['messageType'] == 'SCORE':
            score_form = MessageScoreForm(request.POST)
            if not score_form.is_valid():
                resp['error'] = form.errors
                return JsonResponse(status=400, data=resp)

            new_score = GameScore.objects.create(player=request.user,
                                                 game=game,
                                                 score=score_form.cleaned_data['score'],
                                                 scoreDate=timezone.now())

            # Check if there is a high score for this game, and update it if the new_score is better,
            # or create a new one if there isn't any
            try:
                game_high_score = game.high_score.score
                if new_score.score > game_high_score:
                    Game.objects.filter(pk=game_id).update(high_score=new_score)
            except AttributeError:
                Game.objects.filter(pk=game_id).update(high_score=new_score)

            return JsonResponse(status=201, data=resp)

        elif form.cleaned_data['messageType'] == 'SAVE':
            save_form = MessageSaveForm(request.POST)
            if not save_form.is_valid():
                resp['error'] = form.errors
                return JsonResponse(status=400, data=resp)

            GameState.objects.create(player=request.user,
                                     game=game,
                                     saveDate=timezone.now(),
                                     gameState=save_form.cleaned_data['gameState'])
            return JsonResponse(status=201, data=resp)

        elif form.cleaned_data['messageType'] == 'LOAD_REQUEST':
            load_form = MessageLoadForm(request.POST)
            if not load_form.is_valid():
                resp['error'] = form.errors
                return JsonResponse(status=400, data=resp)

            save_game = GameState.objects.filter(player=request.user, game=game).order_by("-saveDate")

            if save_game.exists():
                resp['result'] = save_game[0].gameState
                return JsonResponse(status=200, data=resp)
            else:
                resp['result'] = None
                resp['error'] = "No save game found."
                return JsonResponse(status=400, data=resp)

        else:
            resp['error'] = 'Invalid message type.'
            return JsonResponse(status=400, data=resp)
    else:
        return HttpResponse(status=405, content='Invalid method.')


def game_add_view(request):
    red_tag = request.GET.get('redirect', None)
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user
            game.save()
            return redirect('/library/')
    else:
        form = GameForm()
    return render(request, 'game/game_form.html', {'form': form, 'redirect': red_tag})


def game_edit_view(request, game_id):
    red_tag = request.GET.get('redirect', None)
    if request.method == 'POST':
        game_to_edit = Game.objects.get(pk=game_id)
        form = GameForm(request.POST, instance=game_to_edit)
        form.save()
        return redirect('/library/')
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


def game_delete_view(request, game_id):
    red_tag = request.GET.get('redirect', None)
    try:
        game = Game.objects.get(pk=game_id)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'redirect': red_tag})

    if request.user == game.developer:
        game.is_active = False
        game.save()
        return redirect('/dev/?redirect=delete')
    return render(request, '404.html', {'redirect': red_tag})


def base_layout(request):
    return render(request, 'base.html')


def game_api_all(request):
    results = Game.objects.filter(is_active=True)
    jsondata = serializers.serialize('json', results)
    return HttpResponse(jsondata)


def game_api_latest(request):
    game = Game.objects.latest('pk')
    data = {
        "game": {
            'id': game.id,
            'name': game.name,
            'genre': game.genre.name,
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
        user2 = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'redirect': red_tag})

    if not user2.is_active:
        return render(request, '404.html', {'redirect': 'inactive'})

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

    # Create temporary transaction and store payment_result with "initialized" state
    transaction = Transaction.objects.create(player=request.user,
                                             game=game,
                                             timestamp=timezone.now(),
                                             payment_reference=0,
                                             payment_result="initialized")
    pid = transaction.pk
    sid = settings.SID
    PAYMENT_SECRET_KEY = settings.PAYMENT_SECRET_KEY
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, game.price, PAYMENT_SECRET_KEY)
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    absolute_payment_url = request.build_absolute_uri(reverse("payment"))
    args = {'game': game, 'redirect': red_tag, 'checksum': checksum, 'sid': sid, 'pid': pid, 'amount': game.price,
            'success_url': absolute_payment_url, 'error_url': absolute_payment_url, 'cancel_url': absolute_payment_url}
    return render(request, 'payment/purchase.html', args)


def payment_result_view(request):
    red_tag = request.GET.get('redirect', None)
    pid_tag = request.GET.get('pid', None)
    reference_tag = request.GET.get('ref', None)
    result_tag = request.GET.get('result', None)
    checksum_tag = request.GET.get('checksum', None)

    # Check if the transaction is valid
    valid_transaction = False
    PAYMENT_SECRET_KEY = settings.PAYMENT_SECRET_KEY
    checksumstr = "pid={}&ref={}&result={}&token={}".format(pid_tag, reference_tag, result_tag, PAYMENT_SECRET_KEY)
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    if checksum_tag == checksum:
        valid_transaction = True

    # Verify the transaction exists
    try:
        transaction = Transaction.objects.get(id=pid_tag)
    except ObjectDoesNotExist:
        return render(request, '404.html', {'redirect': red_tag})

    # Check the user is allowed to manipulate the transaction
    if transaction.player != request.user:
        message = "You are not allowed to manipulate this transaction"
        args = {'game': transaction.game, 'message': message}
        return render(request, 'payment/result.html', args)

    # Check that the result_tag is valid
    if result_tag not in ["success", "cancel", "error"]:
        message = "The payment result was invalid"
        args = {'game': transaction.game, 'message': message}
        return render(request, 'payment/result.html', args)

    # If the payment result was ok add the game to inventory and update the transaction
    if result_tag == "success":
        request.user.inventory.add(transaction.game)
        transaction.payment_result = "success"
        transaction.amount = transaction.game.price
        transaction.payment_reference = reference_tag
        transaction.timestamp = timezone.now()
        transaction.save()

        message = "Thank you for purchasing the game"
        args = {'game': transaction.game,
                'message': message,
                'redirect': red_tag,
                'reference': reference_tag,
                'result': result_tag,
                'validity': valid_transaction}
        return render(request, 'payment/result.html', args)

    # If the payment result was 'cancel' update the transaction
    elif result_tag == "cancel":
        transaction.payment_result = "cancel"
        transaction.payment_reference = reference_tag
        transaction.save()

        message = "The transaction was canceled"
        args = {'game': transaction.game,
                'message': message,
                'redirect': red_tag,
                'reference': reference_tag,
                'result': result_tag,
                'validity': valid_transaction}
        return render(request, 'payment/result.html', args)

    # If the payment result was 'error' update the transaction
    elif result_tag == "error":
        transaction.payment_result = "error"
        transaction.payment_reference = reference_tag
        transaction.save()

        message = "An error occurred while processing the transaction. Please try again"
        args = {'game': transaction.game,
                'message': message,
                'redirect': red_tag,
                'reference': reference_tag,
                'result': result_tag,
                'validity': valid_transaction}
        return render(request, 'payment/result.html', args)
