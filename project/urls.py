from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic.base import TemplateView
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', TemplateView.as_view(template_name='profile/profile.html')),
    path('accounts/profile/', TemplateView.as_view(template_name='profile/profile.html'), name='profile'),
    path('accounts/profile/edit/', views.profile_edit_view, name='profileEdit'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<slug:username>/', views.external_profile_view, name='user_profile'),
]

urlpatterns += [
    path('', views.index_view, name='index'),
    path('library/', views.library_view, name='library'),
    path('explore/', views.explore_view, name='explore'),
    path('game/add/', views.game_add_view, name='gameAdd'),
    path('game/<int:game_id>/', views.game_play_view, name='game'),
    path('game/<int:game_id>/edit/', views.game_edit_view, name='gameEdit'),
    path('game/<int:game_id>/purchase/', views.pay_checkout_view, name='checkout'),
]

urlpatterns += [
    path('payment/', views.payment_result_view, name='payment'),
]
