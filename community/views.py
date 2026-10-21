from django.shortcuts import render, redirect

# Create your views here.

NAME = "TechMate"

def show_forum(request):
    context = {
        'name': NAME,
    }
    return render(request, "forum.html", context)