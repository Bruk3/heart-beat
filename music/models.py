from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User


User = User
users = User.objects.all()
users_list = [(user.id, user.username) for user in users]
users_tuple = tuple(users_list)


class Song(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=1000)
    theme = models.CharField(max_length=1000, blank=True)
    description = models.CharField(max_length=5000)
    is_favorite = models.BooleanField(default=False)
    is_streaming = models.BooleanField(default=False)
    is_suggested_by_user = models.BooleanField(default=False)
    pushed_to = models.IntegerField(choices=users_tuple, default=0)

    def __unicode__(self):
        return self.title + " - " + self.artist

    def __str__(self):
        return self.title 

