from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login


def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("email", "").strip()  # username or phone
        password = request.POST.get("password", "")

        user = None
        try:
            u = User.objects.get(username=identifier)
            user = authenticate(request, username=u.username, password=password)
        except User.DoesNotExist:
            try:
                u = User.objects.get(email=identifier)  # phone stored in email
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            auth_login(request, user)  # call Django's login
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        phone_number = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirmation = request.POST.get("confirmation", "")

        if not username or not phone_number or not password:
            messages.error(request, "All fields are required.")
        elif password != confirmation:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        elif User.objects.filter(email=phone_number).exists():  # using email field for phone
            messages.error(request, "Phone number is already registered.")
        else:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=phone_number,  # storing phone_number in email field
                password=password
            )
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")

    return render(request, "register.html")


@login_required
def home(request):
    return render(request, "base.html")
