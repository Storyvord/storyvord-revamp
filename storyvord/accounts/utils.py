from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from threading import Thread

class EmailThread(Thread):
    def __init__(self, email):
        self.email = email
        Thread.__init__(self)

    def run(self):
        self.email.send()

def send_welcome_email(user):
    email_body = render_to_string('email/welcome.html', {
        'user': user,
    })

    email = EmailMessage(
        subject='Welcome to our platform!',
        body=email_body,
        # from_email=settings.DEFAULT_NO_REPLY_EMAIL,
        from_email='getvishalprajapati@gmail.com',  # Update this line
        to=[user.email],
    )
    email.content_subtype = 'html'

    EmailThread(email).start()