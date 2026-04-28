from django.core.mail.backends.console import EmailBackend
from email import message_from_string
from email.header import decode_header
import quopri

class PrettyConsoleEmailBackend(EmailBackend):
    def write_message(self, message):
        # Récupérer le message MIME complet
        raw = message.message().as_string()

        # Parser le message MIME
        msg = message_from_string(raw)

        # Décoder le sujet
        decoded_headers = decode_header(msg["Subject"])
        decoded_subject = ""
        for header in decoded_headers:
            subject, encoding = header
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
                decoded_subject += subject

        # Décoder le corps
        payload = msg.get_payload()
        body = quopri.decodestring(payload).decode("utf-8")

        print("Contenu brut :")
        print(raw)

        print("Contenu converti")
        print("Sujet :", decoded_subject)
        print("Corps :")
        print(body)
