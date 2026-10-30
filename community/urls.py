from django.urls import path
from community.views import (
    show_forum,
    blog_detail,
    toggle_upvote,
)

app_name = 'community'

urlpatterns = [
    path('forum', show_forum, name='show_forum'),
    path('forum/<slug:blog_slug>/', blog_detail, name='blog_detail'),
    path('forum/<slug:blog_slug>/upvote/', toggle_upvote, name='toggle_upvote'),
]