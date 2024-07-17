from djoser import email

class CustomActivationEmail(email.ActivationEmail):
    # template_name = 'email/custom_activation.html'
    template_name = 'custom_activation.html'

