from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

import datetime

# Create your views here.

NAME = "TechMate"

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    
    context = {
        'name': NAME,
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        'name': NAME,
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def show_main(request):
    context = {
        'name': NAME,
        'welcoming':"Find your need in tech",
        'description': "Temukan perangkat yang pas dengan kebutuhan dan kantong Anda. Bagikan ulasan nyata di komunitas penggemar teknologi, dan buka peluang terbaik untuk menjual gadget lama Anda secara aman. ",
    }
    return render(request, "index.html", context)   