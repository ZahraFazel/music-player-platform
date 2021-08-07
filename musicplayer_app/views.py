# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .forms import *


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    return render(request, 'musicplayer_app/index.html')


@login_required(login_url='/login/')
def my_playlists(request):
    m_playlists = ManagerPlayList.objects.filter(manager=request.user)
    playlists = []
    followed_playlists = []
    follow_or_manage = set()
    other_playlists = []
    for m_playlist in m_playlists:
        found_playlist = False
        for p in playlists:
            if m_playlist.playlist.id == p[0].id:
                p[1] += 1
                found_playlist = True
                break
        if not found_playlist:
            follow_or_manage.add(m_playlist.playlist.id)
            playlists.append((m_playlist.playlist, 1))
    playlist_follower = PlayListFollower.objects.filter(follower=request.user)
    for pf in playlist_follower:
        followed_playlists.append(pf.playlist)
        follow_or_manage.add(pf.playlist.id)
    all_playlists = PlayList.objects.all()
    for playlist in all_playlists:
        if not follow_or_manage.__contains__(playlist.id):
            other_playlists.append(playlist)
    template = loader.get_template('musicplayer_app/playlists.html')
    context = {
        'playlists': playlists,
        'followed_playlists': followed_playlists,
        'other_playlists': other_playlists,
    }
    return HttpResponse(template.render(context, request))


@login_required()
def share_playlist(request, playlist_id):
    if request.method == "POST":
        user_query = Listener.objects.filter(user_ptr_id=User.objects.get(username=request.POST.get('username')).id)
        user = None
        for u in user_query:
            user = u
            break
        if user is not None:
            playlist = PlayList.objects.get(id=playlist_id)
            mp = ManagerPlayList(manager=user, playlist=playlist)
            mp.save()
            return redirect('/playlist/' + str(playlist_id))


@login_required(login_url='/login/')
def add_playlist(request):
    return render(request, 'musicplayer_app/add_playlist_details.html')


@login_required(login_url='/login/')
def add_to_playlist(request, playlist_id):
    if request.method == 'POST':
        music_query = Music.objects.filter(name=request.POST.get('song_name'))
        music = None
        for m in music_query:
            music = m
            break
        if music is not None:
            playlist = PlayList.objects.get(id=playlist_id)
            mp = MusicPlayList(music=music, playlist=playlist)
            mp.save()
            return redirect('/playlist/' + str(playlist_id))


@login_required(login_url='/login/')
def follow(request, playlist_id):
    playlist = PlayList.objects.get(id=playlist_id)
    listener = Listener.objects.get(user_ptr_id=request.user.id)
    if PlayListFollower.objects.filter(playlist=playlist, follower=listener).exists():
        PlayListFollower.objects.filter(playlist=playlist, follower=listener).delete()
    else:
        pf = PlayListFollower(playlist=playlist, follower=listener)
        pf.save()
    return redirect('/playlist/' + str(playlist_id))


# @login_required(login_url='/login/')
def single_playlist(request, playlist_id):
    follow = False
    user = False
    access = False
    if request.user.id is not None:
        if ManagerPlayList.objects.filter(manager=request.user, playlist=PlayList.objects.get(id=playlist_id)).exists():
            access = True
        if PlayListFollower.objects.filter(follower=request.user,
                                           playlist=PlayList.objects.get(id=playlist_id)).exists():
            follow = True
        user = True
    m_songs = MusicPlayList.objects.filter(playlist=PlayList.objects.get(id=playlist_id))
    songs = []
    idx = 1
    playlist = PlayList.objects.get(id=playlist_id)
    for m_song in m_songs:
        songs.append((idx, m_song.music))
        idx += 1
    template = loader.get_template('musicplayer_app/single_playlist.html')
    context = {
        'songs': songs,
        'playlist_id': playlist_id,
        'access': access,
        'playlist_obj': playlist,
        'user': user,
        'follow': follow,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def create_playlist(request):
    if request.method == 'POST':
        ####
        # u = OurUser()
        # u = Listener.objects.get(username=request.POST.get('owner_name'))
        ####
        p = PlayList(name=request.POST.get('playlist_name'), owner=Listener.objects.get(user_ptr_id=request.user.id))
        p.save()
        m = ManagerPlayList(manager=Listener.objects.get(user_ptr_id=request.user.id), playlist=p)
        m.save()
        return index(request)
    return redirect('/my_playlists')


@login_required(login_url='/login/')
def add_music(request):
    if request.method == "POST":
        if request.user.is_artist:
            music_name = request.POST.get('musicname')
            music_artist = request.user
            music_album = request.POST.get('album')
            music_release_date = request.POST.get('release_date')
            print(music_artist)
            m = Music(artist=music_artist, name=music_name, album_name=music_album, release_date=music_release_date,
                      num_stars=0)
            m.save()

        return render(request, 'musicplayer_app/add_music.html/')
    return redirect('/')


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
