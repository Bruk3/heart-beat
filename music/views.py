from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, PushSongForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Song

@login_required
def favorite_songs(request):
    all_songs = Song.objects.all()
    songs = []
    for song in all_songs:
        if request.user.id == song.pushed_to or request.user.id == song.user.id:
            songs.append(song)
    songs_set = set(songs)
    songs = list(songs_set)
    final_songs = []
    for song in songs:
        if song.is_favorite:
            final_songs.append(song)

    context = {
        "songs": final_songs,
        "favorite_songs": "active"
    }
    return render(request, 'music/index.html', context)


@login_required
def recommended_songs(request):
    all_songs = Song.objects.all()
    songs = []
    for song in all_songs:
        if request.user.id == song.pushed_to:
            songs.append(song)
    context = {
        "songs": songs,
        "recommended_songs": "active",
    }
    return render(request, 'music/index.html', context)


@login_required
def pushed_songs(request):
    all_songs = Song.objects.all()
    songs = []
    print("Request.user.id: ", request.user.id)
    for song in all_songs:
        if request.user.id == song.user.id:
            print(song.user.id)
            songs.append(song)
    context = {
        "songs": songs,
        "pushed_songs": "active",
    }
    return render(request, 'music/index.html', context)


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        print(request.POST)
        print(help(form.is_valid))
        if form.is_valid():
            user_name = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create_user(username=user_name, email=email, password=password)
            print("After user creation:", user)
            user.save()
            print("After saving user:", user)
            user = authenticate(username=user_name, password=password)
            print("User has been authenticated")
            print("User is:", user, "It's id is: ", user.id)
            print(dir(user))
            if user is not None:
                print('User is not none.')
                if user.is_active:
                    print("User is active.")
                    login(request, user)
                    songs = Song.objects.filter(user=request.user)
                    return render(request, "music/index.html", {"songs": songs})
            else:
                print("User is none.")
        else:
            print(form.errors)
            print("Form is not valid for singupptoot!")
    print(request.path)
    print(dir(request))
    # for key in request.keys():
    #     print (key, request.key)
    form = UserForm()
    context = {"form": form}
    return render(request, 'music/signup.html', context)


def login_user(request):
    error = None
    if request.method == "POST":
        form = UserForm(request.POST)
        user_name = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=user_name, password=password)
        if user is not None:
            print("User is not None")
            if user.is_active:
                login(request, user)
                print("User is:", request.user, "It's id is: ", request.user.id)
                songs = Song.objects.filter(user=request.user)
                return render(request, "music/index.html", {"songs": songs})
        else:
            print("Incorrect")
            print(form.errors)
            error = "Incorrect user name or password! Please try again"
    form = UserForm()
    context = {
        "form": form,
        "error_message": error
    }
    return render(request, 'music/login.html', context)

@login_required
def logout_user(request):
    logout(request)
    form = UserForm()
    return render(request, "music/login.html", {'form': form})


@login_required
def make_favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if song.is_favorite:
        song.is_favorite = False
    else:
        song.is_favorite = True
    song.save()
    return favorite_songs(request)

# a each_song.split(" ", maxsplit=1)[1].split(">")[0]
@login_required
def delete(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    deleted_song = song.title + " by " + song.artist
    song.delete()
    success_message = "You have successfully deleted the song %s "%deleted_song
    all_songs = Song.objects.all()
    songs = []
    for song in all_songs:
        if request.user.id == song.pushed_to:
            songs.append(song)

    context = {
        "songs": songs,
        "success_message": success_message,
    }
    return render(request, 'music/index.html', context)



@login_required
def push_song(request):
    errors = None
    if request.method == "POST":
        form = PushSongForm(request.POST)
        print(form)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            artist = form.cleaned_data.get('artist')
            pushed_to = form.cleaned_data.get('pushed_to')
            description = form.cleaned_data.get('description')
            user = request.user
            source = form.cleaned_data.get('source')
            print("source:", source, ":endofsource")
            try:
                split_source = source.split('v=')[1].split('&')[0]
                print("Split_source:", split_source)
                real_source = "https://www.youtube.com/embed/" + split_source
                Song.objects.create(title=title, artist=artist, source=real_source, user=user,
                                    description=description, pushed_to=pushed_to)
                pushed_for = User.objects.get(pk=pushed_to)
                song_user = User.objects.filter(id=user.id)
                print("The pusher of this song is:", song_user)
                success_message = "You have successfully pushed the song:-  \"%s\" by \"%s\" to the user \"%s\"" % (title, artist, pushed_for)
            except:
                form = PushSongForm()
                context={
                    "form": form,
                    "error_message": """Sorry, the youtube link you entered is not valid.
                                     Please make sure you copy and paste the whole url.""",
                    "button": "Submit",
                    "push_songs": "active",
                }
                return render(request, 'music/push_song.html', context)




        else:
            errors = form.errors
        context = {
            "form": form,
            "error_message": errors,
            "success_message": success_message,
            "push_songs": "active",
            "button": "Push another song",
        }
        return render(request, 'music/push_song.html', context)
    else:
        if True:
            print(request.user)
            form = PushSongForm()
            for field in form:
                print(field)
            context = {
                "form": form,
                "button": "submit"
            }
            return render(request, 'music/push_song.html', context)
        else:
            print("User is not logged in.")
            form = UserForm()
            return render(request, 'music/login.html', {'form': form})











