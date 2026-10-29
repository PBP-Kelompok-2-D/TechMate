from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from community.models import Blog, Comment
from community.forms import CommentForm

NAME = "TechMate"

def show_forum(request):
    title_query = request.GET.get("title", "").strip()
    blog_list = Blog.objects.all()
    if title_query:
        blog_list = blog_list.filter(title__icontains=title_query)

    context = {
        'name': NAME,
        'blog_list': blog_list,
        'title_query': title_query,
    }
    return render(request, "forum.html", context)

def blog_detail(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("main:login")
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data['content']
            try:
                parent = comment_form.cleaned_data['parent']
            except:
                parent = None
            
            new_comment = Comment(content=content, author=request.user, CommentPost=blog, parent=parent)
            new_comment.save()
            return redirect("community:blog_detail", blog_slug=blog.slug)
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

@login_required(login_url="/login/")
def toggle_upvote(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    if request.method == "POST":
        if request.user in blog.upvoted_by.all():
            blog.upvoted_by.remove(request.user)
        else:
            blog.upvoted_by.add(request.user)
    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("community:show_forum")