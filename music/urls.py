from django.conf.urls import url
from .views import *


app_name = 'music'

urlpatterns = [
    # 'music/index/recommended/
    url(r'^index/recommended/$', recommended_songs, name='recommended_songs'),

    # 'music/index/pushed_songs/
    url(r'^index/pushed_songs/$', pushed_songs, name='pushed_songs'),

    # 'music/index/favorite_songs/
    url(r'^index/favorites/$', favorite_songs, name='favorite_songs'),

    url(r'^$', login_user, name="login"),

    # 'music/login/'
    url(r'^login/$', login_user, name='login'),

    # 'music/logout/'
    url(r'^logout/$', logout_user, name='logout'),

    # 'music/signup/'
    url(r'^signup/$', signup, name='signup'),

    # 'music/<song_id>/make_favorite/'  # action view
    url(r'^(?P<song_id>\d+)/make_favorite/$', make_favorite, name="make_favorite"),

    # '<song_id>/delete/'   # action view
    url(r'^(?P<song_id>\d+)/delete/$', delete, name="delete"),

    # 'music/push_song/'
    url(r'^push_song/$', push_song, name='push_song'),


]