from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    Image = models.ImageField(null=True, blank=True,
                              default='/placeholder.png')
    Name  = models.CharField(max_length=50 , blank=True, null=True)
    Job=models.CharField(max_length=50 , blank=True, null=True)
    Bio =models.CharField(max_length=50 , blank=True, null=True)
    Location =models.CharField(max_length=50 , blank=True, null=True)
    Isverified =models.BooleanField(default=False)
# Create your models here.
    def __str__(self):
        return str(self.user)
@receiver(post_save , sender=User)
def create_user_profile(sender,instance,created , **kwargs):
    if created:
        Profile.objects.create(
            user = instance
        )        





class config(models.Model):

    app_name=models.CharField(max_length=200, null=True, blank=True)
    App_icon=models.ImageField(null=True, blank=True,
                              default='/placeholder.png')
    app_email =models.EmailField(max_length=70,blank=True,unique=True)
    app_phone =models.CharField(max_length=200, null=True, blank=True)
    Maintaince_mode =models.BooleanField(default=True)
    App_account =models.CharField(max_length=200, null=True, blank=True)
    app_version =models.CharField(max_length=200, null=True, blank=True)
    Termes_conditions=models.TextField()
    About_us=models.TextField()
    privacy_policy=models.TextField()

class Playstore_config_class    (models.Model):
       status  =models.BooleanField(default=True)
       Link =models.CharField(max_length=200, null=True, blank=True)
       Playstore_config=models.ForeignKey(config, on_delete=models.SET_NULL, null=True,related_name="playstore")
class appstore_config_class    (models.Model):
       status  =models.BooleanField(default=True)
       Link =models.CharField(max_length=200, null=True, blank=True)
       appstore_config = models.ForeignKey(config, on_delete=models.SET_NULL, null=True,related_name="appstore")

@receiver(reset_password_token_created)

def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):


    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )        




