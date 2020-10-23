from django.contrib import admin
from . models import Genre, Bio, Writeup, Game, Score, Award, Comment, Favourite, Like, Follow
# Register your models here.

admin.site.register(Genre)
admin.site.register(Bio)
admin.site.register(Writeup)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(Award)
admin.site.register(Comment)
admin.site.register(Favourite)
admin.site.register(Like)
admin.site.register(Follow)