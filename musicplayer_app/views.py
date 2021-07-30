# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse

from django.shortcuts import render, redirect
from django.contrib import auth
from .models import OurUser, PlayList ,Music,Artist
# from .forms import AddPlaylist


# Create your views here.
def index(request):


    return render(request, 'musicplayer_app/index.html')


def add_playlist(request):
    return render(request, 'musicplayer_app/add_playlist_details.html')


def create_playlist(request):
    if request.method == 'POST':
        ####
        # u = OurUser()
        u = OurUser.objects.get(username=request.POST.get('owner_name'))
        ####
        p = PlayList(name=request.POST.get('playlist_name'), owner=u)
        p.save()
        return index(request)
    return add_playlist(request)


def add_music(request):
    if request.method == "POST":
        music_name = request.POST.get('musicname')
        music_artist = request.user
        music_album = request.POST.get('album')
        music_release_date = request.POST.get('release_date')
        print(music_artist)
        m = Music(artist=music_artist,name= music_name,album_name = music_album,release_date=music_release_date,num_stars=0)
        m.save()

    return render(request, 'musicplayer_app/add_music.html/')


def register(request):
    if request.method == "POST":
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                OurUser.objects.get(username=request.POST.get('username'))
                return render(request, 'musicplayer_app/register.html', {'error': 'Username is already taken!'})
            except OurUser.DoesNotExist:
                user = OurUser.objects.create_user(username=request.POST.get('username'),
                                                   password=request.POST.get('password1'))
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'musicplayer_app/register.html', {'error': 'Password does not match!'})
    else:
        return render(request, 'musicplayer_app/register.html')


def login(request):
    if request.method == 'POST':
        password = request.POST['password']
        username = request.POST['username']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'musicplayer_app/login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'musicplayer_app/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('home')



def artist_profile(request):


    all_musics = Music.objects.filter(artist_id = 3)
    # print(all_musics)
    # print(""""-------------------------------------------------------------------------""")
    return render(request, 'musicplayer_app/artist_profile.html' , {'tracks':all_musics})


def remove_track(request):
    if request.method =='GET':
        trackId = request.GET.get('id')
        print("track_id",trackId)
        Music.objects.filter(id = trackId).delete()
    return artist_profile(request)

def upload(request):
    if request.method == "POST":
        music_name = request.POST.get('musicname')
        music_artist = request.user
        music_album = request.POST.get('album')
        music_release_date = request.POST.get('release_date')
        print(music_artist)
        m = Music(artist=music_artist,name= music_name,album_name = music_album,release_date=music_release_date,num_stars=0)
        m.save()


    return render(request,'musicplayer_app/upload.html')
