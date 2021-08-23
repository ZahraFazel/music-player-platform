from .models import *


class RecommenderSystem:
    def __init__(self, username):
        self.user = Listener.objects.get(username=username)
        self.recommendations = []

    def recommend(self):
        playlists = list(PlayList.objects.filter(owner__username=self.user.username).values_list('name', flat=True))
        genres = {}
        musics = set()
        for playlist in playlists:
            playlist_musics = list(MusicPlayList.objects.filter(playlist__name=playlist).values_list('music__id', flat=True))
            for music in playlist_musics:
                musics.add(music)
        if self.user.vip:
            for music in musics:
                music_genres = list(MusicGenres.objects.filter(music__id=music).values_list('genre', flat=True))
                for genre in music_genres:
                    if genre not in genres.keys():
                        genres[genre] = 0
                    genres[genre] += 1
            top_genres = sorted(genres, key=genres.get, reverse=True)[:3]
            if len(top_genres) > 0:
                music_ids = set(MusicGenres.objects.filter(genre__in=top_genres).values_list('music_id', flat=True))
            else:
                music_ids = set(MusicGenres.objects.all().values_list('music_id', flat=True))
        else:
            music_ids = set(MusicGenres.objects.all().values_list('music_id', flat=True))
        selected = music_ids - music_ids.intersection(musics)
        self.recommendations = Music.objects.filter(id__in=selected)
