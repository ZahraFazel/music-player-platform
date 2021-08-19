from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [

    path('artist/<int:artistId>', views.single_artist, name='single_artist'),
    path('playlist/<int:playlist_id>', views.single_playlist, name='single_playlist'),
    path('add_to_playlist/<int:playlist_id>', views.add_to_playlist, name='add_to_playlist'),
    path('follow/<int:playlist_id>', views.follow, name='follow'),
    path('share_playlist/<int:playlist_id>', views.share_playlist, name="share_playlist"),
    url(r'upload/', views.upload, name='upload'),
    url(r'setplaylist_play/', views.setplaylist_play, name='setplaylist_play'),
    url(r'artist_profile/', views.artist_profile, name='artist_profile'),
    url(r'create_new_playlist/', views.create_playlist, name='add_music'),
    # url(r'add_music/', views.add_music, name='add_music'),
    url(r'add_playlist/', views.add_playlist),
    url(r'musicplayer_app/', views.index, name='index'),
    url(r'login/', views.login, name='login'),
    url(r'register/', views.register, name='register'),
    url(r'logout/', views.logout, name='logout'),
    url(r'^remove_track/$', views.remove_track,name='remove_track'),

    url(r'artists/', views.artists_page, name='artists_page'),

    url(r'^follow_artist/$', views.follow_artist, name='follow_artist'),
    url(r'followed_artists/', views.followed_artists, name='followed_artists'),

    url(r'^unfollow_artist/$', views.unfollow_artist, name='unfollow_artist'),
    url(r'artist_followers/', views.artist_followers, name='artist_followers'),

    url(r'^artist_single_page/$', views.artist_single_page, name='artist_single_page'),

    url(r'^my_playlists/$', views.my_playlists, name='my_playlists'),
    # url(r'', views.start),
    path('profile/', views.profile, name='profile'),
    path('premium/', views.premium, name='premium'),
    path('purchase/', views.purchase, name='purchase'),
    path('get_assets/', views.get_assets, name='get_assets'),
    path('edit_porfile/', views.edit_profile, name='edit_profile'),
    path('royalty/', views.royalty, name='royalty'),

    path('search/',views.search,name = 'search'),

]
