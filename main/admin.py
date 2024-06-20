from django.contrib import admin



from .models import Track, Genre, Artist


admin.site.register(Track)
admin.site.register(Genre)
admin.site.register(Artist)
