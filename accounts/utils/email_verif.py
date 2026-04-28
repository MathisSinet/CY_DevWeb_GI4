from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.http import HttpRequest

signer = TimestampSigner()

def generate_verification_token(user):
    return signer.sign(user.pk)

def verify_token(token, max_age=60*60*24):  # 24h
    try:
        user_id = signer.unsign(token, max_age=max_age)
        return int(user_id)
    except (BadSignature, SignatureExpired):
        return None

def send_verification_email(user, request: HttpRequest):
    token = generate_verification_token(user)
    print(token)
    verification_url = request.build_absolute_uri(
        reverse("verify_email") + f"?token={token}"
    )

    send_mail(
        subject="Vérifiez votre adresse email",
        message=f"Merci de vous être inscrit à Coconimal. Cliquez ici pour vérifier votre email : {verification_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
