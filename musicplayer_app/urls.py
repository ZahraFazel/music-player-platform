from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [

    path('artist/<int:artistId>', views.single_artist, name='single_artist'),
    url(r'artists/', views.artists_page, name='play_q'),
    path('playlist/<int:playlist_id>', views.single_playlist, name='single_playlist'),
    path('add_to_playlist/<int:playlist_id>', views.add_to_playlist, name='add_to_playlist'),
    path('follow/<int:playlist_id>', views.follow, name='follow'),
    path('share_playlist/<int:playlist_id>', views.share_playlist, name="share_playlist"),
    url(r'upload/', views.upload, name='upload'),
    url(r'play_q/', views.play_q, name='play_q'),
    url(r'artist_profile/', views.artist_profile, name='artist_profile'),
    url(r'create_new_playlist/', views.create_playlist, name='add_music'),
    # url(r'add_music/', views.add_music, name='add_music'),
    url(r'add_playlist/', views.add_playlist),
    url(r'musicplayer_app/', views.index, name='index'),
    url(r'login/', views.login, name='login'),
    url(r'register/', views.register, name='register'),
    url(r'logout/', views.logout, name='logout'),
    url(r'^remove_track/$', views.remove_track,name='remove_track'),
    # url(r'^follow_artist/(?P<id>\d{0,50})/$', views.follow_artist, name='follow_artist'),

    url(r'^follow_artist/$', views.follow_artist, name='follow_artist'),
    url(r'^my_playlists/$', views.my_playlists, name='my_playlists'),
    # url(r'', views.start),
    path('profile/', views.profile, name='profile'),
    path('premium/', views.premium, name='premium'),
    path('purchase/', views.purchase, name='purchase')
]
