# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse

from django.shortcuts import render
from  .models import Music

# Create your views here.
def index(request):
    return render(request, 'musicplayer_app/index.html')


def add_playlist(request):
    return render(request, 'musicplayer_app/add_playlist.html')


def add_music(request):

    if request.method == "POST":
        music_name  = request.POST.get('musicname')
        music_artist = request.POST.get('artist')
        music_release_date = request.POST.get('release_date')

        # m = Music(artist=music_artist,name= music_name,release_date=music_release_date,num_stars=0)
        # m.save()


    return  render(request , 'musicplayer_app/add_music.html/')

