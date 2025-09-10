# instax/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),         # feed
    path('accounts/', include('accounts.urls')),  # login/registro
]
