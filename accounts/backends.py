from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthBackend(ModelBackend):
    """Backend pour authentifier par email au lieu de username"""
    
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            # Si un email est fourni, on l'utilise pour retrouver l'utilisateur
            if email:
                user = User.objects.get(email=email)
            elif username:
                # Sinon on utilise le username
                user = User.objects.get(username=username)
            else:
                return None
        except User.DoesNotExist:
            return None
        
        # Vérifier le mot de passe
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
