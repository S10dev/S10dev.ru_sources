from django.urls import path
from . import views
from Users.views import upload_avatar


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_post, name='new_post'),
    path('group/<slug:slug>', views.group_posts, name='group'),
    path('<str:username>/upload_avatar/', upload_avatar, name='upload_avatar'),
    path(
        "follow/",
        views.follow_feed,
        name="follow_feed"
        ),
    path(
        "<str:username>/follow/",
        views.profile_follow,
        name="profile_follow"
        ),
    path(
        "<str:username>/unfollow/",
        views.profile_unfollow,
        name="profile_unfollow"
        ),
    path(
        '<str:username>/',
        views.profile,
        name='profile'
        ),
    path(
        '<str:username>/<int:post_id>/',
        views.post_view,
        name='post'
        ),
    path(
        '<str:username>/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'
        ),
    path(
        "<username>/<int:post_id>/comment",
        views.add_comment,
        name="add_comment"
        ),
]
