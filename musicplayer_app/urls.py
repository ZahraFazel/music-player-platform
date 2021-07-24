from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'new_playlist/', views.add_playlist),
    url(r'musicplayer_app/', views.index),
]