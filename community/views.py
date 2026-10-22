from django.shortcuts import render, redirect, get_object_or_404
from community.models import Blog, Comment

# Create your views here.

NAME = "TechMate"

def show_forum(request):
    blog_list = Blog.objects.all()
    context = {
        'name': NAME,
        'blog_list': blog_list,
    }
    return render(request, "forum.html", context)

def blog_detail(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    blogs_comments = Comment.objects.filter(CommentPost=blog)
    context = {
        'name': NAME,
        'blog': blog,
        'comments': blogs_comments,
    }
    return render(request, 'blog.html', context)