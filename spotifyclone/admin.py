from django.contrib import admin
from .models import Song, Music, Album
# Register your models here.

admin.site.register(Song)
admin.site.register(Music)
admin.site.register(Album)