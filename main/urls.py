from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', index, name='index_url'),
    path('artists', artists, name='artists_url'),
    path('genres', genres, name='genres_url'),
    path('genre/<str:slug>', genre_detail, name='genre_detail_url'),
    path('artist_page/<str:slug>/', artist_page, name='artist_page_url'),
    path('list/<str:tp>', listt, name='list_url'),
    path('track_detail/<str:slug>/', track_detail, name='track_detail_url'),
    path('search', search, name='search_url')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





