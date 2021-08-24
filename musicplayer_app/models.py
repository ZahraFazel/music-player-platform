# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.forms import CharField


class User(AbstractUser):
    name = models.CharField(max_length=100, default="Unknown")
    email = models.EmailField(unique=True, null=False)
    is_artist = models.BooleanField(default=False)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profiles/')


class Listener(User):
    vip = models.BooleanField(default=False)
    vip_end = models.DateField(default='1990-01-01')


class Artist(User):
    asset = models.IntegerField(default=0)


class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    Album_name = models.CharField(max_length=100, default='album_name')
    release_date = models.DateField()
    num_stars = models.IntegerField()
    quality = models.IntegerField(default=1)
    cover = models.ImageField(blank=True, null=True, upload_to='pictures/')
    file = models.FileField(blank=True, null=True, upload_to='trackes/')



class PlayList(models.Model):
    owner = models.ForeignKey(Listener, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='My Playlist')


class MusicPlayList(models.Model):
    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("playlist", "music"),)


class ManagerPlayList(models.Model):
    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    manager = models.ForeignKey(Listener, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("playlist", "manager"),)


class ArtistFollower(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    follower = models.ForeignKey(Listener, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("artist", "follower"),)


class PlayListFollower(models.Model):
    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    follower = models.ForeignKey(Listener, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("playlist", "follower"),)


class MusicGenres(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)

    class Meta:
        unique_together = (("music", "genre"),)
