from django.urls import path
#from .views import YouTubeSearchView
from django.urls import path
from .views import oauth2_login, oauth2_callback
from django.contrib import admin
from django.urls import path
from .views import oauth2_login, oauth2_callback,get_user_videos


urlpatterns = [
   
]

urlpatterns = [
    #path('search/', YouTubeSearchView.as_view(), name='youtube-search'),
    path('oauth2login/', oauth2_login, name='oauth2_login'),
    path('oauth2callback/', oauth2_callback, name='oauth2_callback'),
    path('api/youtube/videos/',  get_user_videos, name='user_videos'),  # Assure-toi que cette route existe aussi
]
