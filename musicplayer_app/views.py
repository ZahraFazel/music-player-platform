# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse

from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'musicplayer_app/index.html')


def add_playlist(request):
    return render(request, 'musicplayer_app/add_playlist.html')
