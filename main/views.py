from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import PermissionDenied  

from main.models import Profile, Report
from main.forms import ProfileForm, ReportForm
import datetime

# Create your views here.

NAME = "TechMate"

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        created_user = form.save()
        Profile.objects.create(user=created_user, avatar="", bio="No bio yet")
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
    last_login = request.COOKIES.get('last_login', 'No log section yet / Cookie not found')
    context = {
        'name': NAME,
        'welcoming':"Find your need in tech",
        'description': "Temukan perangkat yang pas dengan kebutuhan dan kantong Anda. Bagikan ulasan nyata di komunitas penggemar teknologi, dan buka peluang terbaik untuk menjual gadget lama Anda secara aman. ",
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_user_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    viewed_user = profile.user
    last_login = request.COOKIES.get('last_login', 'No log section yet / Cookie not found')
    edit_form =  ProfileForm(instance=profile)
    context = {
        'name': NAME,
        "profile": profile,
        "viewed_user": viewed_user,
        "edit_form": edit_form,
        "report_form": ReportForm(),
        "last_login": last_login,
    }
    return render(request, "user_profile.html", context)

@login_required(login_url="/login/")
def edit_user_profile(request, profile_id):  
    profile = get_object_or_404(Profile, pk=profile_id)
    viewed_user = profile.user
    
    if not request.user.is_superuser and request.user != viewed_user:
        raise PermissionDenied
    
    form = ProfileForm(request.POST or None, instance=profile)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile telah berhasil diperbarui!")
        return redirect("main:show_user_profile", profile_id=profile.id)
    
    context = {
        "name": NAME,
        "form": form,
        "profile": profile,
    }
    return render(request, "profile_update_form.html", context)

@require_POST
def edit_user_profile_ajax(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)

    if not request.user.is_superuser and request.user != profile.user:
        return JsonResponse(
            {"message": "Anda tidak memiliki izin untuk mengubah profil ini."},
            status=403,
        )

    form = ProfileForm(request.POST, instance=profile)
    if form.is_valid():
        profile = form.save()
        return JsonResponse(
            {
                "message": "Profil berhasil diperbarui.",
                "avatar": profile.avatar or "",
                "bio": profile.bio,
            },
            status=200,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@require_POST
def report_user_ajax(request, profile_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Silakan login untuk melaporkan pengguna."},
            status=403,
        )

    profile = get_object_or_404(Profile, pk=profile_id)

    if request.user == profile.user:
        return JsonResponse(
            {"message": "Anda tidak dapat melaporkan diri sendiri."},
            status=403,
        )

    form = ReportForm(request.POST)
    if form.is_valid():
        report = form.save(commit=False)
        report.reporter = request.user
        report.reported_user = profile.user
        report.save()
        return JsonResponse({"message": "Laporan berhasil dikirim."}, status=201)
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)