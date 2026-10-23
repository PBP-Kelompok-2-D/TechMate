from django.shortcuts import render, redirect, get_object_or_404
from community.models import Blog, Comment
from community.forms import CommentForm

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
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data['content']
            try:
                parent = comment_form.cleaned_data['parent']
            except:
                parent=None
            
            new_comment = Comment(content=content, author=request.user, CommentPost=blog, parent=parent)
            new_comment.save()
            return redirect("community:blog_detail", slug=blog.slug)
    else:
        comment_form = CommentForm()
        

    blogs_comments = Comment.objects.filter(CommentPost=blog)
    context = {
        'name': NAME,
        'blog': blog,
        'comments': blogs_comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog.html', context)