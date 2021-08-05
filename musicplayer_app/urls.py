from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'upload/', views.upload, name='upload'),
    url(r'artist_profile/', views.artist_profile, name='artist_profile'),
    url(r'create_new_playlist/', views.create_playlist, name='add_music'),
    url(r'add_music/', views.add_music, name='add_music'),
    url(r'add_playlist/', views.add_playlist),
    url(r'musicplayer_app/', views.index, name='index'),
    url(r'login/', views.login, name='login'),
    url(r'register/', views.register, name='register'),
    url(r'logout/', views.logout, name='logout'),
    url(r'^remove_track/$', views.remove_track,name='remove_track'),

]
