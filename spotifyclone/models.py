from django.db import models
from .validators import validate_is_audio
from .helper import get_audio_length
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Song(models.Model):
    title = models.TextField()
    artist = models.TextField()
    image = models.ImageField()
    audio_file = models.FileField(blank=True, null=True)
    audio_link = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=20)
    paginate_by = 2

    def __str__(self):
        return self.title


class Music(models.Model):
    title = models.CharField(max_length=500)
    artiste = models.CharField(max_length=500)
    album = models.ForeignKey('Album', on_delete=models.SET_NULL, null=True, blank=True)
    time_length = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    audio_file = models.FileField(upload_to='musics/', validators=[validate_is_audio])
    cover_image = models.ImageField(upload_to='music_images/')

    def save(self, *args, **kwargs):
        if not self.time_length:
            # logic for getting length of audio
            audio_length = get_audio_length(self.audio_file)
            self.time_length = f'{audio_length:.2f}'

        return super().save(*args, **kwargs)

    class META:
        ordering = "id"


class Album(models.Model):
    name = models.CharField(max_length=400)


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

