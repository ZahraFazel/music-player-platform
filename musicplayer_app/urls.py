from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'add_music/', views.add_music, name='add_music'),
    url(r'add_playlist/', views.add_playlist),
    url(r'musicplayer_app/', views.index, name='home'),
    url(r'login/', views.login, name='login'),
    url(r'register/', views.register, name='register')
]
