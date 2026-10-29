# urls.py — Connects a URL to the explorer_search view. Because the main
# project (techmate/urls.py) already includes this file under 'explorer/',
# the empty path '' here makes the page available at /explorer.

from django.urls import path

from . import views

# Lets templates refer to this page as 'explorer:explorer_search'.
app_name = 'explorer'

urlpatterns = [
    # /explorer/ -> the explorer_search view (handles GET and POST).
    path('', views.explorer_search, name='explorer_search'),
]
