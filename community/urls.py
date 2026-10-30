from django.urls import path
from . import views

# Baris ini wajib ditambahkan agar Django mengenali namespace 'community'
app_name = 'community'

urlpatterns = [
    # --- Rute untuk Forum Diskusi ---
    # name='forum_list' diubah menjadi 'show_forum' agar cocok dengan base.html temanmu
    path('', views.forum_list, name='show_forum'),
    path('thread/baru/', views.create_thread, name='create_thread'),
    path('thread/<slug:slug>/', views.forum_detail, name='forum_detail'),
    path('thread/<slug:slug>/edit/', views.edit_thread, name='edit_thread'),
    path('thread/<slug:slug>/hapus/', views.delete_thread, name='delete_thread'),
    path('thread/<int:blog_id>/komentar/', views.add_comment, name='add_comment'),
    
    # --- Rute untuk AJAX Upvote ---
    path('thread/<int:blog_id>/upvote/', views.upvote_thread, name='upvote_thread'),
    
    # --- Rute untuk Sistem Rating & Review ---
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/baru/', views.create_review, name='create_review'),
]