from django.urls import path
from . import views

app_name = 'App1_Core'

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/<tag>/', views.home, name='categories'),
    path('post/postdetail/<pk>/', views.post_detail, name='post-detail'),

    path('create_post/', views.create_post, name='create-post'),
    path('post/postedit/<pk>/', views.editPost, name='editpost'),
    path('post/deletepost/<pk>/', views.delete_post, name='deletepost'), 

    path('comment_sent/<pk>/', views.comment_sent, name='commentsent'),
    path('delete_comment/<pk>/', views.comment_delete, name='delete-comment'),
    path('reply_sent/<pk>/', views.reply_sent, name='reply-sent'),
    path('reply/reply_delete/<pk>/', views.reply_delete, name='reply-delete'),

    path('post/like/<pk>/', views.like_post, name='like-post'),
    path('comment/like_comment/<pk>/', views.like_comment, name='comment-like'),
    path('reply/like_reply/<pk>/', views.like_reply, name='like-reply'),
]