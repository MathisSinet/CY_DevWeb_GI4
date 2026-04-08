from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm

def signup_view(request: HttpRequest):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # connexion automatique
            return redirect("login")
        else:
            messages.error(request, "Formulaire invalide!" + str(form.error_messages))
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

def login_view(request: HttpRequest):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Identifiants invalides")

    return render(request, "login.html")

def logout_view(request: HttpRequest):
    logout(request)
    return redirect("login")