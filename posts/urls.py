# posts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('start/', views.start, name='start'),
    path('logout/', views.logout_temp, name='logout_temp'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('purge/', views.purge_now, name='purge_now'),  # opcional para probar
]
