from django.urls import path
from .views import *

app_name = 'map'

urlpatterns = [
    path('library/', LibrarySearchView.as_view()),
]