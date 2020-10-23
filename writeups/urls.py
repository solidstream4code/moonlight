from django.urls import path
from . import views

app_name = 'writeups'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login', views.Login.as_view(), name='login'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('dashboard/<username>', views.Dashboard.as_view(), name='dashboard'),
    path('write', views.Write.as_view(), name='write'),
    path('edit/<pk>', views.EditWriteup.as_view(), name='edit'),
    path('delete/<pk>', views.DeleteWriteup.as_view(), name='delete'),
    path('about/<username>', views.About.as_view(), name='about'),
    path('update/about/<username>', views.UpdateAbout.as_view(), name='update_about'),
    path('writeup/<pk>', views.WriteupDisplay.as_view(), name='writeup'),
    path('comment/<pk>', views.AddComment.as_view(), name='comment'),
    path('like/<pk>', views.LikeWriteup.as_view(), name='like'),
    path('favourite/<pk>', views.FavWriteup.as_view(), name='favourite'),
    path('follow/<follow>', views.FollowAuthor.as_view(), name='follow'),
    path('unfollow/<username>', views.UnFollowAuthor.as_view(), name='unfollow'),
    path('read/<genre>/<sort>', views.Read.as_view(), name="read"),
    path('popular/<genre>', views.PopularRead.as_view(), name="popular"),
    path('favourites/<genre>', views.FavouriteRead.as_view(), name="favourites"),
    path('writings/<username>/<genre>', views.AuthorRead.as_view(), name="author_read"),
    path('following/<username>', views.Following.as_view(), name='followings'),
    path('followers/<username>', views.Follower.as_view(), name='followers'),
    path('logout', views.user_logout, name='logout')
]
