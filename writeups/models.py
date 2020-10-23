from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Writeup(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    text = models.TextField()
    note = models.TextField(blank=True)
    draft = models.BooleanField(default=False, help_text="Do you want to save this writeup as draft?")
    time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0, blank=False)
    favourites = models.IntegerField(default=0, blank=False)
    comments = models.IntegerField(default=0, blank=False)
    views = models.IntegerField(default=0, blank=False)

    def get_absolute_url(self):
        return reverse("writeups:writeup", args=(self.id, ))

    def __str__(self):
        return self.title


class Bio(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True)
    school = models.CharField(max_length=250, null=True)
    age = models.IntegerField(null=True)
    quote = models.TextField(null=True)
    genre = models.CharField(max_length=250, null=True)
    mobile_no = models.CharField(max_length=250, null=True)
    photo = models.FileField(blank=True)

    def get_absolute_url(self):
        return reverse("writeups:about", args=(self.author.username,))

    def __str__(self):
        return self.author.username


class Game(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.game


class Score(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.game + "  " + self.score


class Award(models.Model):
    awards = ['Gold', 'Silver', 'Bronze']
    writeup = models.ForeignKey(Writeup, on_delete=models.CASCADE)
    #award = models.CharField(widget=models.ChoiceField(awards))
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.writeup.title + "  " + self.award


class Comment(models.Model):
    writeup = models.ForeignKey(Writeup, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[0:100]

    def comment(self):
        writeup = Writeup.objects.get(pk=self.writeup.pk)
        writeup.comments = writeup.comments + 1
        writeup.save()


class Favourite(models.Model):
    admirer = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Writeup, on_delete=models.CASCADE)

    def unique_entry(self):
        try:
            Favourite.objects.filter(admirer=self.admirer).get(post=self.post)
            return False
        except:
            return True

    def __str__(self):
        return "{} favourites {}".format(self.admirer.username, self.post.title)

    def favourite(self):
        writeup = Writeup.objects.get(pk=self.post.pk)
        writeup.favourites = writeup.favourites + 1
        writeup.save()


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Writeup, on_delete=models.CASCADE)

    def __str__(self):
        return "{} likes {}".format(self.liker.username, self.post.title)

    def unique_entry(self):
        try:
            Like.objects.filter(liker=self.liker).get(post=self.post)
            return False
        except:
            return True

    def like(self):
        writeup = Writeup.objects.get(pk=self.post.pk)
        writeup.likes = writeup.likes + 1
        writeup.save()


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    follow = models.CharField(max_length=250, blank=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} follows {}".format(self.follower.username, self.follow)

    def unique_entry(self):
        try:
            Follow.objects.filter(follower=self.follower).get(follow=self.follow)
            return False
        except:
            return True