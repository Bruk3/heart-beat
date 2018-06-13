from django.db import models


class Song(models.Model):
    artist = models.CharField(max_length=250)
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=1000)
    theme = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000)
    is_favorite = models.BooleanField(default=False)
    is_streaming = models.BooleanField(default=False)
    is_suggested_by_user = models.BooleanField(default=False)
    is_suggested_for_user = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " - " + self.artist

