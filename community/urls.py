from django.urls import path
from community.views import (
        show_forum,
)

app_name = 'community'

urlpatterns = [
    path('forum', show_forum, name='show_forum'),
]