# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    return render(request, 'musicplayer_app/index.html')


@login_required(login_url='/login/')
def add_playlist(request):
    return render(request, 'musicplayer_app/add_playlist_details.html')


@login_required(login_url='/login/')
def create_playlist(request):
    if request.method == 'POST':
        ####
        # u = OurUser()
        u = Listener.objects.get(username=request.POST.get('owner_name'))
        ####
        p = PlayList(name=request.POST.get('playlist_name'), owner=u)
        p.save()
        return index(request)
    return add_playlist(request)


@login_required(login_url='/login/')
def add_music(request):
    if request.method == "POST":
        music_name = request.POST.get('musicname')
        music_artist = request.user
        music_album = request.POST.get('album')
        music_release_date = request.POST.get('release_date')
        print(music_artist)
        m = Music(artist=music_artist, name=music_name, album_name=music_album, release_date=music_release_date,
                  num_stars=0)
        m.save()

    return render(request, 'musicplayer_app/add_music.html/')


@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render(request, 'musicplayer_app/register.html')
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration is completed!')
            return HttpResponseRedirect('/login/')
        return HttpResponse(f"{form.errors}")


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'musicplayer_app/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            dj_login(request, user)
            messages.success(request, 'You are now logged in as {}!'.format(username))
            return HttpResponseRedirect('/musicplayer_app/')
        return HttpResponse('Wrong password/username')


@csrf_exempt
@login_required(login_url='/login/')
def logout(request):
    if request.method == 'POST':
        dj_logout(request)
        messages.success(request, 'Logout successfully!')
        return HttpResponseRedirect('/login/')


def artist_profile(request):
    all_musics = Music.objects.filter(artist_id=3)
    # print(all_musics)
    # print(""""-------------------------------------------------------------------------""")
    return render(request, 'musicplayer_app/artist_profile.html', {'tracks': all_musics})


def remove_track(request):
    if request.method == 'GET':
        trackId = request.GET.get('id')
        print("track_id", trackId)
        Music.objects.filter(id=trackId).delete()
    return artist_profile(request)


def upload(request):
    if request.method == "POST":
        music_name = request.POST.get('musicname')
        music_artist = request.user
        music_album = request.POST.get('album')
        music_release_date = request.POST.get('release_date')
        print(music_artist)
        m = Music(artist=music_artist, name=music_name, album_name=music_album, release_date=music_release_date,
                  num_stars=0)
        m.save()

    return render(request, 'musicplayer_app/upload.html')
