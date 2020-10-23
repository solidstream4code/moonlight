from .models import Genre, Bio, Favourite, Writeup, Comment, Like, Follow
from django.contrib.auth.models import User


def get_all_genres():
    genres = Genre.objects.all()
    return genres


def get_user_details(username):
    user = User.objects.get(username=username)
    bio = Bio.objects.get(author__username=username)

    details = {
        'username': user.username,
        'email': user.email,
        'firstname': user.first_name,
        'lastname': user.last_name,
        'mobile_no': bio.mobile_no,
        'bio': bio.bio,
        'school': bio.school,
        'age': bio.age,
        'quote': bio.quote,
        'genre': bio.genre,
        'photo': bio.photo
    }

    return details


def get_writeups(genre, sort):
    if genre == 'all':
        writeups = Writeup.objects.all().filter(draft=False)
    else:
        writeups = Writeup.objects.filter(genre__name=genre).filter(draft=False)

    if sort == 'fav':
        writeups = writeups.order_by('favourites').reverse()
    elif sort == 'recent':
        writeups = writeups.order_by('time').reverse()
    elif sort == 'comments':
        writeups = writeups.order_by('comments').reverse()
    elif sort == 'likes':
        writeups = writeups.order_by('likes').reverse()

    return writeups


def get_user_writeups(username, genre):
    if genre == 'all':
        writeups = User.objects.get(username=username).writeup_set.filter(draft=False)
    else:
        writeups = User.objects.get(username=username).writeup_set.filter(genre__name=genre).filter(draft=False)
    return writeups


def get_popular_writeups(genre):
    if genre == 'all':
        writeups = Writeup.objects.filter(draft=False).order_by('views').reverse()
    else:
        writeups = Writeup.objects.filter(genre__name=genre).filter(draft=False).order_by('views')
    return writeups


def get_favourite_writeups(request, genre):
    if request.user.is_authenticated:
        if genre == 'all':
            writeups = Favourite.objects.filter(post__draft=False).filter(admirer=request.user)
        else:
            writeups = Favourite.objects.filter(post__draft=False).filter(admirer=request.user).filter(post__genre__name=genre)
        return writeups
    else:
        return ''


def check_followed(follower, follow):
    if follower.is_authenticated:
        elem = Follow.objects.filter(follow=follow).filter(follower=follower)
    else:
        elem = False

    if elem:
        return True
    else:
        return False