# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class OurUser(User):
    # name = models.CharField(max_length=20, null=False)
    # password = models.CharField(max_length=16, null=False)
    # email = models.EmailField(max_length=50, unique=True, null=False)
    vip = models.BooleanField(default=False)
    charge = models.IntegerField(default=0)


class Artist(models.Model):
    artist_name = models.CharField(max_length=80)
    password = models.CharField(max_length=16)
    asset = models.IntegerField()


class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    Album_name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()


class PlayList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='My Playlist')


class MusicPlayList(models.Model):
    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("playlist", "music"),)


class ManagerPlayList(models.Model):
    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("playlist", "manager"),)


class ArtistFollower(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("artist", "follower"),)


class PlayListFollower(models.Model):
    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("playlist", "follower"),)
