from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django.conf import settings
from threading import Thread
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User
import jwt

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
def send_verification_email(user, token, absurl=None):
    if not absurl:
        absurl = f"{settings.SITE_URL}accounts/v2/email-verify/?token={token}"
    email_body = render_to_string('email/verification.html', {
        'user': user.email,
        'absurl': absurl,
    })
    email = EmailMessage(subject="Activate your account", body=email_body, from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email])
    email.content_subtype = "html"
    EmailThread(email).start()
    
def send_password_reset_email(email, request):
    user = User.objects.filter(email=email).first()
    if user:
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        abs_url = f'{settings.SITE_URL}/password-reset-confirm/{uidb64}/{token}'
        email_body = render_to_string('email/password_reset.html', {
            'abs_url': abs_url, 
            'user': user.email
        })
        email = EmailMessage(subject='Reset your password', body=email_body, from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email])
        email.content_subtype = 'html'
        EmailThread(email).start()
        
def verify_email_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None
    
def send_welcome_email(user):
    email_body = render_to_string('email/welcome.html', {
        'user': user,
    })

    email = EmailMessage(
        subject='Welcome to our platform!',
        body=email_body,
        from_email=getattr(settings, 'DEFAULT_NO_REPLY_EMAIL', 'getvishalprajapati@gmail.com'),  # Use settings value or fallback
        to=[user.email],
    )
    email.content_subtype = 'html'

    EmailThread(email).start()

class EmailThread(Thread):
    def __init__(self, email):
        self.email = email
        Thread.__init__(self)

    def run(self):
        self.email.send()
    
