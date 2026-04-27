from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import SignupForm
from datetime import timedelta

def signup_view(request: HttpRequest):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # connexion automatique
            return redirect("index")
        else:
            messages.error(request, "Formulaire invalide!" + str(form.error_messages))
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user:
            if user.last_login and user.last_login < timezone.now() - timedelta(hours = 3):
                user.add_points(10)
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Identifiants invalides")

    return render(request, "login.html")

def logout_view(request: HttpRequest):
    logout(request)
    return redirect("login")

@login_required
def modif_view(request: HttpRequest):
    if request.method == "POST":
        #pour changer mot de passe : donner l'ancien d'abord
        password = request.POST["password"].strip()
        new_password = request.POST["new_password"].strip()
        confirm_password = request.POST["confirm_password"].strip()

        if not request.user.check_password(password):
            messages.error(request, "Mot de passe incorrect")
            return render(request, "modif.html")

        if confirm_password != new_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return render(request, "modif.html")
        
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, "Mot de passe modifié !")

        return redirect("login")
    
    return render(request, "modif.html")

@login_required
def profile_view(request: HttpRequest):
    if request.method == "POST":
        first_name = request.POST["name"].strip()
        last_name = request.POST["surname"].strip()
        email = request.POST["email"].strip()

        if not first_name or not last_name or not email:
            messages.error(request, "Aucun champ ne doit être vide !")
            return render(request, "profile.html")

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email 

        request.user.save()
        messages.success(request, "Modification réussite !")

        return redirect("profile")
    
    return render(request, "profile.html")
