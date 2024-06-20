from django.db import models
from django.urls import reverse
import os


class Track(models.Model):


    name = models.CharField(max_length=70, db_index=True)
    audio = models.FileField(upload_to='tracks/')
    date_pub = models.DateTimeField(auto_now_add=True)
    artists = models.ManyToManyField('Artist', 'tracks')
    genre = models.ManyToManyField('Genre', 'tracks')
    views = models.IntegerField(default=0)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    lang = models.CharField(max_length=10, default='foreign', db_index=True)
    text = models.TextField(blank=True, default='Текст песни пока не добавлен!')

    def get_absolute_url(self):
        return reverse('track_detail_url', kwargs={'slug':self.slug})

    

    def get_name_for_download(self):
        res = ''
        for artist in self.artists.all():
            res += artist.name
            res += ','
        return res[:-1] + ' - ' + self.name + '(mp3.ru).mp3'



    def __str__(self):
        return self.name


class Artist(models.Model):

    name = models.CharField(max_length=70, db_index=True)
    image = models.ImageField(upload_to='images/')
    date_pub = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    
    def get_best_track(self):
        res = self.tracks.all().order_by('-views')[:1]
        return res


    def get_absolute_url(self):
        return reverse('artist_page_url', kwargs = {'slug' : self.slug})


    def __str__(self):
        return self.name



class Genre(models.Model):

    
    name = models.CharField(max_length=30, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)


    def get_absolute_url(self):
        return reverse('genre_detail_url', kwargs={'slug': self.slug})


    def __str__(self):
        return self.name
