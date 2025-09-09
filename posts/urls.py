from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('user/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
]
