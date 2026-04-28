from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import password_validation
from django.utils import timezone
from datetime import timedelta
from .models import User
from .forms import SignupForm
from .utils.email_verif import send_verification_email, verify_token

def signup_view(request: HttpRequest):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # connexion automatique
            send_verification_email(user, request)
            return redirect("check_email")
        else:
            messages.error(request, "Formulaire invalide !" + str(form.error_messages))
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
        
        try:
            password_validation.validate_password(new_password, request.user)
        except Exception as e:
            messages.error(request, str(e))
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

        if not first_name or not last_name:
            messages.error(request, "Aucun champ ne doit être vide !")
            return render(request, "profile.html")

        request.user.first_name = first_name
        request.user.last_name = last_name

        request.user.save()
        messages.success(request, "Modification réussie !")

        return redirect("profile")
    
    return render(request, "profile.html")

def verify_email_view(request: HttpRequest):
    token = request.GET.get("token")
    user_id = verify_token(token)

    if not user_id:
        verif_message = "Lien invalide ou expiré."
        return render(request, "verify_email.html", {verif_message: verif_message})

    user = get_object_or_404(User, pk=user_id)
    user.verified = True
    user.save()

    verif_message = "Votre adresse email a été vérifiée avec succès !"
    return render(request, "verify_email.html", {"verif_message": verif_message})

@login_required
def check_email_view(request: HttpRequest):
    # Si l'utilisateur est déjà vérifié, rediriger vers le profil
    if request.user.is_authenticated and request.user.verified:
        return redirect("profile")

    if request.method == "POST":
        # Option pour renvoyer un nouveau lien
        send_verification_email(request.user, request)
        messages.success(request, "Un nouveau lien de vérification a été envoyé à votre adresse email.")

    return render(request, "check_email.html")