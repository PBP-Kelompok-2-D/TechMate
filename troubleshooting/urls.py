from django.urls import path
from . import views

app_name = 'troubleshooting'

urlpatterns = [
    path('', views.troubleshooting_list, name='article_list'),
    path('api/filter/', views.filter_articles_ajax, name='filter_articles_ajax'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('api/bookmark/<int:article_id>/', views.toggle_bookmark_ajax, name='toggle_bookmark_ajax'),
    path('api/feedback/<int:article_id>/', views.submit_feedback_ajax, name='submit_feedback_ajax'),
    path('api/feedback/delete/<int:feedback_id>/', views.delete_feedback_ajax, name='delete_feedback_ajax'),
]