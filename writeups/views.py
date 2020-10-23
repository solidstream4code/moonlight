from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import LoginForm, RegForm, WriteupForm
from .utiliity import get_all_genres, get_user_details, get_writeups, get_favourite_writeups, get_user_writeups
from .utiliity import get_popular_writeups, get_favourite_writeups, check_followed
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Writeup, Genre, Comment, Like, Favourite, Follow, Bio
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class Index(View):
    def get(self, request):
        return render(request, "writeups/index.html", {})


class Login(View):
    form_data = LoginForm()
    genres = get_all_genres()

    def get(self, request):
        return render(request, "writeups/login.html", {'forms': self.form_data, 'genres': self.genres})

    def post(self, request):
        form_data = LoginForm(request.POST)

        if form_data.is_valid():
            username = form_data.cleaned_data['username']
            password = form_data.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('writeups:dashboard', username)
            else:
                return render(request, "writeups/login.html", {'forms': form_data, 'genres': self.genres})

        return render(request, "writeups/login.html", {'forms': form_data, 'genres': self.genres})


class Signup(View):
    form = RegForm()
    genres = get_all_genres()
    template = "writeups/signup.html"

    def get(self, request):
        return render(request, self.template, {'forms': self.form, 'genres': self.genres})

    def post(self, request):
        form = RegForm(request.POST)

        if form.is_valid():
            user = User()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['surname']

        try:
            user.save()
            new_bio = Bio(author=user)
            new_bio.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('writeups:dashboard', user.username)
            else:
                return render(request, self.template,
                              {'forms': form, 'error': 'The username and the password do not match'})

        except IntegrityError:
            return render(request, self.template, {'forms': form, 'error': 'The username has already been taken. '
                                                                           'Please pick a new username'})


class Dashboard(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        user_details = get_user_details(username)

        followed = check_followed(follower=request.user, follow=username)

        poems = user.writeup_set.all().filter(genre__name=Genre.objects.get(name="Poetry")).filter(
            draft=False).order_by(
            'time').reverse()
        essays = user.writeup_set.all().filter(genre__name=Genre.objects.get(name="Essay")).filter(
            draft=False).order_by(
            'time').reverse()
        folklores = user.writeup_set.all().filter(genre__name=Genre.objects.get(name="Folklore")).filter(
            draft=False).order_by(
            'time').reverse()
        short_stories = user.writeup_set.all().filter(genre__name=Genre.objects.get(name="Short Story")).filter(
            draft=False).order_by('time').reverse()

        context = {
            'poems': poems,
            'essays': essays,
            'folklores': folklores,
            'short_stories': short_stories,
            'user_details': user_details,
            'request_user': user,
            'followed': followed
        }

        return render(request, "writeups/dashboard.html", context)


class Write(View):
    form = WriteupForm()
    template = "writeups/writeup_form.html"
    
    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template, {'form': self.form})

    @method_decorator(login_required)
    def post(self, request):
        form = WriteupForm(request.POST)

        if form.is_valid():
            author = User.objects.get(id=request.user.id)
            genre = form.cleaned_data['genre']
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            note = form.cleaned_data['note']
            draft = form.cleaned_data['draft']

            writeup = Writeup(author=author, genre=genre, title=title, text=text, note=note, draft=draft)

            try:
                writeup.save()
                return redirect(writeup)
            except:
                return render(request, self.template, {'form': form})

        else:
            return render(request, self.template, {'form': form})
            

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class EditWriteup(UpdateView):
    model = Writeup
    fields = ['genre', 'title', 'text', 'note', 'draft']
    template_name = 'writeups/writeup_edit_form.html'


class DeleteWriteup(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        object = Writeup.objects.get(pk=pk)
        user = object.author

        object.delete()
        return redirect("writeups:dashboard", user.username)


class About(View):
    @method_decorator(login_required)
    def get(self, request, username):
        user_details = get_user_details(username)
        user = User.objects.get(username=username)

        context = {
            'user_details': user_details,
            'request_user': user,
            'followed': check_followed(request.user, username)
        }

        return render(request, "writeups/about.html", context)


class WriteupDisplay(View):
    def get(self, request, pk):
        writeup = Writeup.objects.get(id=pk)
        owner_user = writeup.author
        comments = Comment.objects.filter(writeup=writeup).order_by('time').reverse()
        likes = Like.objects.filter(post=writeup)
        favourites = Favourite.objects.filter(post=writeup)
        other_writeups = owner_user.writeup_set.all().order_by('time').reverse()

        context = {
            'writeup': writeup,
            'owner_user': owner_user,
            'comments': comments,
            'likes': likes,
            'favourites': favourites,
            'other_writeups': other_writeups
        }

        if request.user.is_authenticated and request.user.username != owner_user.username:
            writeup.views += 1
            writeup.save()

        return render(request, 'writeups/writeup.html', context)


class AddComment(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        poster = request.user
        writeup = Writeup.objects.get(pk=pk)
        text = request.POST['text']

        comment = Comment(poster=poster, writeup=writeup, text=text)
        comment.save()
        comment.comment()

        return redirect("writeups:writeup", pk=pk)


class FavWriteup(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        admirer = request.user
        post = Writeup.objects.get(pk=pk)

        fav_instance = Favourite(admirer=admirer, post=post)

        if fav_instance.unique_entry():
            fav_instance.save()
            fav_instance.favourite()

        return redirect("writeups:writeup", pk=pk)


class LikeWriteup(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        admirer = request.user
        post = Writeup.objects.get(pk=pk)

        like_instance = Like(liker=admirer, post=post)

        if like_instance.unique_entry():
            like_instance.save()
            like_instance.like()

        return redirect("writeups:writeup", pk=pk)


class FollowAuthor(View):
    @method_decorator(login_required)
    def get(self, request, follow):
        follower = request.user

        follow_object = Follow(follow=follow, follower=follower)
        if follow_object.unique_entry():
            follow_object.save()

        return redirect("writeups:about", username=follow)


class UnFollowAuthor(View):
    @method_decorator(login_required)
    def get(self, request, username):

        object = Follow.objects.get(follow=username)
        object.delete()

        return redirect("writeups:about", username=username)


class Read(View):
    def get(self, request, genre, sort):
        writeups = get_writeups(genre, sort)
        favourites = {}

        if request.user.is_authenticated:
            favourites = get_favourite_writeups(request, 'all')

        paginator = Paginator(writeups, 10)
        page_no = request.GET.get('page')

        context = {
            'page_obj': paginator.get_page(page_no),
            'favourites': favourites,
            'genre': genre
        }
        return render(request, "writeups/read.html", context)


class AuthorRead(View):
    def get(self, request, username, genre):
        writeups = get_user_writeups(username, genre)
        favourites = {}

        if request.user.is_authenticated:
            favourites = get_favourite_writeups(request, 'all')

        paginator = Paginator(writeups, 10)
        page_no = request.GET.get('page')

        context = {
            'page_obj': paginator.get_page(page_no),
            'favourites': favourites,
            'genre': genre,
            'username': username
        }
        return render(request, "writeups/author_read.html", context)


class PopularRead(View):
    def get(self, request, genre):
        writeups = get_popular_writeups(genre)
        favourites = {}

        if request.user.is_authenticated:
            favourites = get_favourite_writeups(request, 'all')

        paginator = Paginator(writeups, 10)
        page_no = request.GET.get('page')

        context = {
            'page_obj': paginator.get_page(page_no),
            'favourites': favourites,
            'genre': genre
        }
        return render(request, "writeups/popular_read.html", context)


class FavouriteRead(View):
    def get(self, request, genre):
        if request.user.is_authenticated:
            favourites = get_favourite_writeups(request, genre)

            paginator = Paginator(favourites, 10)
            page_no = request.GET.get('page')
            page = paginator.get_page(page_no)
        else:
            page = {}

        if page:
            context = {
                'page_obj': page,
                'favourites': favourites,
                'genre': genre
            }
        else:
            context = {
                'favourites': favourites,
                'genre': genre
            }

        return render(request, "writeups/favourite_reads.html", context)
        

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class UpdateAbout(UpdateView):
    model = Bio
    fields = ['bio', 'school', 'age', 'quote', 'genre', 'mobile_no', 'photo']
    template_name = 'writeups/about_update.html'



class Following(View):
    def get(self, request, username):
        authors = []

        follows = Follow.objects.filter(follower__username=username)

        for follow_obj in follows:
            user = User.objects.get(username=follow_obj.follow)
            bio = Bio.objects.get(author__username=follow_obj.follow)
            time = follow_obj.time

            each = {
                'bio': bio,
                'user': user,
                'time': time
            }

            authors.append(each)

        paginator = Paginator(authors, 30)
        page_no = request.GET.get('page')
        page = paginator.get_page(page_no)

        context = {
            'authors': page,
            'requested_user': username
        }

        return render(request, 'writeups/followings.html', context)


class Follower(View):
    def get(self, request, username):
        authors = []

        follows = Follow.objects.filter(follow=username)

        for follow_obj in follows:
            user = User.objects.get(username=follow_obj.follow)
            bio = Bio.objects.get(author__username=follow_obj.follow)
            time = follow_obj.time

            each = {
                'bio': bio,
                'user': user,
                'time': time
            }

            authors.append(each)

        paginator = Paginator(authors, 30)
        page_no = request.GET.get('page')
        page = paginator.get_page(page_no)

        context = {
            'authors': page,
            'requested_user': username
        }

        return render(request, 'writeups/followers.html', context)


def user_logout(request):
    logout(request)

    return redirect("writeups:index")
