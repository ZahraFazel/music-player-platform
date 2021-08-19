# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from distutils.command import register

from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder

from .forms import *
import datetime
import calendar
from django.db.models import Q
from django.core import serializers
import json
from django.core import serializers

# Create your views here.
def start(request):
    return HttpResponseRedirect('/login/')

def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__


@login_required(login_url='/login/')
def index(request):

    if Listener.objects.filter(user_ptr_id=request.user.id).exists():
        current_user_id =  Listener.objects.get(user_ptr_id=request.user.id).id

        playlist_id = PlayList.objects.filter(owner_id=current_user_id)[4].id

        musicplaylist = MusicPlayList.objects.filter(playlist_id=playlist_id)
        playlist=[]
        for p in musicplaylist:
            m = Music.objects.get(id=p.music_id)

            playlist.append(
                {
                    "title":m.name,
                    "album":m.Album_name,
                    "artist":Artist.objects.get(id=m.artist_id).username,
                    "image":"/media/"+m.cover.name,
                    "file":"/media/"+m.file.name,

                }

            )

        playlist=json.dumps(playlist,default=json_default)
        # playlist = serializers.serialize("json", playlist)

        return render(request,'musicplayer_app/index.html' , {"playlist":playlist})
    else:
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
            playlists.append((m_playlist.playlist, len(MusicPlayList.objects.filter(playlist=m_playlist.playlist))))
    playlist_follower = PlayListFollower.objects.filter(follower=request.user)
    for pf in playlist_follower:
        followed_playlists.append((pf.playlist, len(MusicPlayList.objects.filter(playlist=pf.playlist))))
        follow_or_manage.add(pf.playlist.id)
    all_playlists = PlayList.objects.all()
    for playlist in all_playlists:
        if not follow_or_manage.__contains__(playlist.id):
            other_playlists.append((playlist, len(MusicPlayList.objects.filter(playlist=playlist))))
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


# def add_music(request):
#     if request.method == "POST":
#         if request.user.is_artist:
#             music_name = request.POST.get('musicname')
#             music_artist = request.user
#             music_album = request.POST.get('album')
#             music_release_date = request.POST.get('release_date')
#             print(music_artist)
#             m = Music(artist=music_artist, name=music_name, album_name=music_album, release_date=music_release_date,
#                       num_stars=0)
#             m.save()
#
#         return render(request, 'musicplayer_app/add_music.html/')
#     return redirect('/')


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
    if request.method == 'POST' or request.method == 'GET':
        dj_logout(request)
        messages.success(request, 'Logout successfully!')
        return HttpResponseRedirect('/login/')


@login_required(login_url='/login/')
def artist_profile(request):

    all_musics = Music.objects.filter(artist_id=request.user.id)

    artistId = Artist.objects.get(id=request.user.id)
    followers_of_artist = ArtistFollower.objects.filter(artist_id=artistId)
    return render(request, 'musicplayer_app/artist_profile.html', {'tracks': all_musics ,'count_of_followers':len(followers_of_artist)})


@login_required(login_url='/login/')
def remove_track(request):
    if request.method == 'GET':
        trackId = request.GET.get('id')
        Music.objects.filter(id=trackId).delete()
    return artist_profile(request)


@login_required(login_url='/login/')
def upload(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        if user.is_artist:
            music_name = request.POST.get('musicname')
            music_artist = Artist.objects.get(user_ptr_id=request.user.id)
            music_album = request.POST.get('album')
            music_release_date = request.POST.get('release_date')
            music_quality = request.POST.get('quality')
            music_cover = request.FILES.get('cover')
            music_file = request.FILES.get('music_file')
            m = Music(artist=music_artist, name=music_name, Album_name=music_album, release_date=music_release_date,
                      num_stars=0,quality=music_quality,cover=music_cover,file=music_file)
            m.save()

    return render(request, 'musicplayer_app/upload.html/')
    # return redirect('/')


    return HttpResponse('Quality changed')


@login_required(login_url='/login/')
def artists_page(request):
    all_artist = Artist.objects.all()
    return render(request, 'musicplayer_app/artist.html', {'artists': all_artist})


@login_required(login_url='/login/')
def artist_single_page(request):

    if request.method == 'GET':
         artist_ID = request.GET.get('id')
         artist = Artist.objects.get(id=artist_ID)
         musics = Music.objects.filter(artist_id=artist_ID)

         followers_of_artist = ArtistFollower.objects.filter(artist_id=artist_ID)
         user_is_following =False

         if ArtistFollower.objects.filter(artist=artist_ID,follower=Listener.objects.get(user_ptr_id=request.user.id)).exists():
            user_is_following =True

    context = {'artist': artist , 'musics':musics , 'followers_count': len(followers_of_artist) , 'followers':followers_of_artist ,  'user_is_following':user_is_following}
    return render(request,'musicplayer_app/artist_single.html' ,context)


@login_required(login_url='/login/')
def follow_artist(request):
    if request.method == 'GET':
        artistId = request.GET.get('id')

        artist = Artist.objects.get(id=artistId)
        listener = Listener.objects.get(user_ptr_id=request.user.id)
        if ArtistFollower.objects.filter(artist=artist, follower=listener).exists():
            print("already followed")
        else:
            Af = ArtistFollower(artist=artist, follower=listener)
            Af.save()

    return redirect('/artist/' + str(artistId))


@login_required(login_url='/login/')
def unfollow_artist(request):
    if request.method == 'GET':
        artistId = request.GET.get('id')

        artist = Artist.objects.get(id=artistId)
        listener = Listener.objects.get(user_ptr_id=request.user.id)
        if ArtistFollower.objects.filter(artist=artist, follower=listener).exists():
            ArtistFollower.objects.filter(artist=artist, follower=listener).delete()
            print("Unfollowed!!!")

    return redirect('/artist/' + str(artistId))


def artist_followers(request):

    artistId = Artist.objects.get(id=request.user.id)

    followers_of_artist = ArtistFollower.objects.filter(artist_id=artistId)
    followers =[]
    for f in followers_of_artist:
        l = Listener.objects.get(id=f.follower_id)
        followers.append(l)
    return render(request,'musicplayer_app/artist_followers.html' , {"followers_of_artist":followers})

def followed_artists(request):

        listenerId = Listener.objects.get(id=request.user.id)
        followed__artist = ArtistFollower.objects.filter(follower_id=listenerId)
        followed_artists =[]
        for f in followed__artist:
            l = Artist.objects.get(id=f.artist_id)
            followed_artists.append(l)

        return render(request,'musicplayer_app/followed_artists.html', {"followed_artists":followed_artists})

@login_required(login_url='/login/')
def single_artist(request,artistId ):

    artist = Artist.objects.get(id=artistId)
    musics = Music.objects.filter(artist_id=artistId)

    followers_of_artist = ArtistFollower.objects.filter(artist_id=artistId)
    user_is_following =False

    if ArtistFollower.objects.filter(artist=artistId,follower=Listener.objects.get(user_ptr_id=request.user.id)).exists():
        user_is_following =True

    context = {'artist': artist , 'musics':musics , 'followers_count': len(followers_of_artist) ,  'user_is_following':user_is_following}
    return render(request,'musicplayer_app/artist_single.html' ,context)


@csrf_exempt
@login_required(login_url='/login/')
def profile(request):
    user = User.objects.get(username=request.user.username)
    print(user.is_artist)
    if user.is_artist:
        return render(request, 'musicplayer_app/artist_profile.html')
    else:
        return render(request, 'musicplayer_app/profile.html')


@login_required(login_url='/login/')
def premium(request):
    return render(request, 'musicplayer_app/purchase.html')


@csrf_exempt
@login_required(login_url='/login/')
def purchase(request):
    if request.method == 'POST':
        user = Listener.objects.get(username=request.user.username)
        print(user.username)
        print(user.vip)
        num_months = 0
        if request.POST['plan'] == 'one':
            num_months = 1
        elif request.POST['plan'] == 'three':
            num_months = 3
        elif request.POST['plan'] == 'six':
            num_months = 6
        elif request.POST['plan'] == 'year':
            num_months = 12
        if user.vip:
            year, month, day = map(int, user.vip_end.split('-'))
            source_date = datetime.date(year, month, day)
        else:
            source_date = datetime.date.today()
        month = source_date.month - 1 + num_months
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(source_date.day, calendar.monthrange(year, month)[1])
        print(year)
        print(month)
        print(day)
        user.vip_end = '{}-{}-{}'.format(year, month, day)
        print(user.vip_end)
        user.vip = True
        user.save()
        messages.success(request, 'Purchased successfully!')
        return redirect('/profile/')


@login_required(login_url='/login/')
def get_assets(request):
    return render(request, 'musicplayer_app/royalty.html')


@csrf_exempt
@login_required(login_url='/login/')
def royalty(request):
    if request.method == 'POST':
        user = Artist.objects.get(username=request.user.username)
        user.asset = 0
        user.save()
        return redirect('/profile/')


@csrf_exempt
@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email') or None
        new_password1 = request.POST.get('new_password1') or None
        new_password2 = request.POST.get('new_password2') or None
        user = User.objects.get(username=request.user.username)
        if new_email is not None:
            user.email = new_email
        if new_password1 is not None:
            if new_password1 == new_password2:
                user.set_password(new_password1)
            else:
                return HttpResponse('Password does not match!')
        user.save()
        return redirect('/musicplayer_app/')











def search(request):
    query = None
    results =[]
    if request.method == 'GET':

        query = request.GET.get("search_text")
        if query:
            if Artist.objects.filter(username=query).exists():
                a = Artist.objects.get(username=query)
                match_id = a.id
                return redirect('/artist_single_page/?id='+str(match_id))


            elif Music.objects.filter(name=query).exists() or Music.objects.filter(Album_name=query).exists():
                results = Music.objects.filter(Q(name = query) | Q(Album_name = query))
                for x in results:
                    x.artist_id  =Artist.objects.get(id=x.artist_id).username
                return  render(request,'musicplayer_app/search_results.html' , {'results':results})

            else:
                print("NO match found")




    return HttpResponse(status=204)




@login_required(login_url='/login/')
def setplaylist_play(request):
    current_user_id =  Listener.objects.get(user_ptr_id=request.user.id).id
    quality= request.POST.get('quality')

    playlist_id = PlayList.objects.filter(owner_id=current_user_id)[0].id

    playlist = MusicPlayList.objects.filter(playlist_id=playlist_id)

    print("PLAYLIST",playlist)
    return redirect('musicplayer_app/index.html' , {"playlist":playlist})
