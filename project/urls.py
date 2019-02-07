from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

from app import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('admin/', admin.site.urls),
    url('', include('pwa.urls')),
    path('base_layout/', views.base_layout)
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('account/', include('django.contrib.auth.urls')),
    path('account/signup/', views.signup_view, name='signup'),
    path('account/activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('account/activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account/profile/', TemplateView.as_view(template_name='profile/profile.html'), name='profile'),
    path('account/profile/edit/', views.profile_edit_view, name='profileEdit'),
]

urlpatterns += [
    path('profile/', TemplateView.as_view(template_name='profile/profile.html')),
    path('profile/<slug:username>/', views.external_profile_view, name='user_profile'),
]

urlpatterns += [
    path('explore/', views.explore_view, name='explore'),
    path('library/', views.library_view, name='library'),
    path('dev/', views.library_view, name='dev'),
    path('game/add/', views.game_add_view, name='gameAdd'),
    path('game/<int:game_id>/', views.game_play_view, name='game'),
    path('game/<int:game_id>/edit/', views.game_edit_view, name='gameEdit'),
    path('game/<int:game_id>/delete/', views.game_delete_view, name='gameDelete'),
    path('game/<int:game_id>/purchase/', views.pay_purchase_view, name='purchase'),
]

urlpatterns += [
    path('payment/', views.payment_result_view, name='payment'),
]

urlpatterns += [
    path('api/game/all/', views.game_api_all, name='api_game_all'),
    path('api/game/latest/', views.game_api_latest, name='api_game_latest')
]

urlpatterns += [
    path('api/v1/', include('api.urls')),
]
