from django.shortcuts import render
from django.http import HttpResponse

from .models import Artist, Track, Genre

import os
from django.conf import settings

def index(request):
    
    
    top_artists = Artist.objects.all().order_by('-views')[:5]

    new_tracks = Track.objects.all().order_by('-date_pub')[:10]
    

    new_left_tracks = []
    new_right_tracks = []
    fl = True

    for track in new_tracks:
        if fl == True:
            new_left_tracks.append(track)
            fl = False
        else:
            new_right_tracks.append(track)
            fl = True

    popular_tracks = Track.objects.all().order_by('-views')[:10]
    
    popular_left_tracks = []
    popular_right_tracks = []
    fl = True

    for track in popular_tracks:
        if fl == True:
            popular_left_tracks.append(track)
            fl = False
        else:
            popular_right_tracks.append(track)
            fl = True

    return render(request, 'main/index.html',
        context=
        {
            'top_artists' : top_artists,
            'new_left_tracks' : new_left_tracks,
            'new_right_tracks' : new_right_tracks,
            'popular_left_tracks' : popular_left_tracks,
            'popular_right_tracks' : popular_right_tracks,
        }
    )


def genres(request):


    genres = Genre.objects.all().order_by('name')
    
    top_artists = Artist.objects.all().order_by('-views')[:5]


    return render(request, 'main/genres.html',
        context=
        {
            'genres' : genres,
            'top_artists' : top_artists,
        }
    )


def artists(request):
    

    top_artists = Artist.objects.all().order_by('-views')[:5]

    artists = Artist.objects.all().order_by('name')

    right_artists = []
    left_artists = []

    fl = True

    for artist in artists:
    
        if fl == True:
            left_artists.append(artist)
            fl = False
        else:
            right_artists.append(artist)
            fl = True
    
    return render(request, 'main/artists.html',
        context=
        {
            'left_artists' : left_artists,
            'right_artists' : right_artists,
            'top_artists' : top_artists,
        }
    )



def artist_page(request, slug):
    artist = Artist.objects.get(slug__iexact=slug)
    
    top_artists = Artist.objects.all().order_by('-views')[:5]


    left_tracks = []
    right_tracks = []
    fl = True
        
    for track in artist.tracks.all():
        if fl == True:
            left_tracks.append(track)
            fl = False
        else:
            right_tracks.append(track)
            fl = True
    
    return render(request, 'main/artist_page.html',
        context=
        {
            'artist' : artist,
            'left_tracks' : left_tracks,
            'right_tracks' : right_tracks,
            'top_artists' : top_artists,
        }
    )





def listt(request, tp):
    tracks = None
    page_title = None
    if tp == 'popular':
        tracks = Track.objects.all().order_by('-views')
        page_title = 'Популярные'
    elif tp == 'foreign':
        tracks = Track.objects.filter(lang__iexact='foreign').order_by('-views')
        page_title = 'Зарубежные'
    else:
        tracks = Track.objects.all().order_by('-date_pub')
        page_title = 'Новые'
                
    top_artists = Artist.objects.all().order_by('-views')[:5]


    left_tracks = []
    right_tracks = []
    fl = True

    for track in tracks:
        if fl == True:
            left_tracks.append(track)
            fl = False
        else:
            right_tracks.append(track)
            fl = True


    return render(request, 'main/list.html',        
        context=
        {
            'top_artists' : top_artists,
            'page_title' : page_title,
            'left_tracks' : left_tracks,
            'right_tracks' : right_tracks,
        }
    ) 




def genre_detail(request, slug):

    top_artists = Artist.objects.all().order_by('-views')[:5]
    genre = Genre.objects.get(slug__iexact=slug)

    left_tracks = []
    right_tracks = []
    fl = True
    
    for track in genre.tracks.all():
        if fl == True:
            left_tracks.append(track)
            fl = False
        else:
            right_tracks.append(track)
            fl = True

    return render(request, 'main/list.html',
        context=
        {
            'page_title' : genre.name,
            'left_tracks' : left_tracks,
            'right_tracks' : right_tracks,
            'top_artists' : top_artists,
        }
    )


def track_detail(request, slug):

    track = Track.objects.get(slug__iexact=slug)

    track.views += 1
    
    track.save()

    for artist in track.artists.all():

        artist.views += 1
        artist.save()

    
    top_artists = Artist.objects.all().order_by('-views')[:5]
    
    from mutagen.mp3 import MP3 
    try:
        audio_path = os.path.join(settings.MEDIA_ROOT, track.audio.name)
        audio = MP3(audio_path)
    except FileNotFoundError:
        return HttpResponseNotFound("Файл не найден")
    except Exception as e:
        return HttpResponseServerError(f"Ошибка обработки аудио файла: {str(e)}")

    length = audio.info.length // 1
    minutes = int(length // 60)
    seconds = int(length % 60)
    formatted_length = f"{minutes:02}:{seconds:02}"
    
    return render(request, 'main/track_detail.html',
        context=
        {
            'track' : track,
            'top_artists' : top_artists,
            'formatted_length': formatted_length
        }
    )



def search(request):

    q = request.GET.get('q', '')

    tracks = None
    page_title = 'Результаты поиска'

    tracks = Track.objects.filter(name__icontains=q)
    
    left_tracks = []
    right_tracks = []
    fl = True

    for track in tracks:
        if fl == True:
            left_tracks.append(track)
            fl = False
        else:
            right_tracks.append(track)
            fl = True

    return render(request, 'main/list.html',
        context=
        {
            'page_title' : page_title,
            'left_tracks' : left_tracks,
            'right_tracks' : right_tracks,
        }
    )
