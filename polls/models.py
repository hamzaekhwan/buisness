from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete,pre_save
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.conf import settings

class favorite(models.Model):
    user_id = models.CharField(max_length=50 , blank=True, null=True)
    favoriteUser_id=models.CharField(max_length=50 , blank=True, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    Image = models.ImageField(null=True, blank=True)
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

       
@receiver(pre_save, sender=Profile)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.user:
        existing_image = Profile.objects.get(user=instance.user)
        if instance.Image and existing_image.Image != instance.Image:
            existing_image.Image.delete(False)

class Custom_button(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    title=models.CharField(max_length=50 , blank=True, null=True)
    icon=models.ImageField(null=True, blank=True   )
    color=models.CharField(max_length=50 , blank=True, null=True,default="#0000FF")
    isActive=models.BooleanField(default=False)
def __str__(self):
        return str(self.user)
@receiver(post_save , sender=User)
def create_user_custom_buttton(sender,instance,created , **kwargs):
    if created:
        Custom_button.objects.create(
            user = instance
        )
            

class Vcard(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image=models.ImageField(null=True, blank=True   )
    first_name=models.CharField(max_length=50 , blank=True, null=True)
    last_name=models.CharField(max_length=50 , blank=True, null=True)

    email=models.CharField(max_length=50 , blank=True, null=True)
    phone=models.CharField(max_length=50 , blank=True, null=True)
    address=models.CharField(max_length=50 , blank=True, null=True)
    city=models.CharField(max_length=50 , blank=True, null=True)
    state=models.CharField(max_length=50 , blank=True, null=True)
    zip=models.CharField(max_length=50 , blank=True, null=True)
    country=models.CharField(max_length=50 , blank=True, null=True)
    company=models.CharField(max_length=50 , blank=True, null=True)
    title=models.CharField(max_length=50 , blank=True, null=True)
    website=models.CharField(max_length=50 , blank=True, null=True)
    notes=models.CharField(max_length=50 , blank=True, null=True)
    vcf_file=models.FileField(blank=True)
    isActive=models.BooleanField(default=False)

     

@receiver(post_save , sender=User)
def create_user_Vcard(sender,instance,created , **kwargs):
    if created:
        Vcard.objects.create(
            user = instance
        )   


@receiver(pre_save, sender=Vcard)
def delete_old_image_Vcard(sender, instance, *args, **kwargs):
    if instance.user:
        existing_image = Vcard.objects.get(user=instance.user)
        if instance.image and existing_image.image != instance.image:
            existing_image.image.delete(False)  


@receiver(pre_save, sender=Vcard)
def delete_old_file(sender, instance, *args, **kwargs):
    if instance.user:
        existing_file = Vcard.objects.get(user=instance.user)
        if instance.vcf_file and existing_file.vcf_file != instance.vcf_file:
            existing_file.vcf_file.delete(False)                         

class config(models.Model):

    app_name=models.CharField(max_length=200, null=True, blank=True)
    App_icon=models.ImageField(null=True, blank=True)
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
             
SECTION_NUM = (
  ('1', 'Social media'),
  ('2','Contact info'),
  ('3','For Business'),
  ('4','Payments'),
  ('5','Content'),
  ('6','Music'),
  ('7','More'),

)

TYPE_OF_LINK=(
    ('1','username'),
    ('2','link'),
)

class platforms(models.Model):
    isActive=models.BooleanField(default=True)
    name =models.CharField(max_length=200, null=True, blank=True)
    domain=models.CharField(max_length=200, null=True, blank=True)
    dialog_title=models.CharField(max_length=200, null=True, blank=True)
    link_type=section=models.CharField(max_length=50,choices=TYPE_OF_LINK)
    error_message=models.CharField(max_length=200, null=True, blank=True)
    color1=models.CharField(max_length=50 , blank=True, null=True,default="#0000FF")
    color2=models.CharField(max_length=50 , blank=True, null=True,default="#0000FF")
    section=models.CharField(max_length=50,choices=SECTION_NUM)
    info=models.TextField()
    image=models.FileField(blank=True)
    
    def __str__(self):
        return str(self.name)
        
@receiver(pre_save, sender=platforms)
def delete_old_image_platforms(sender, instance, *args, **kwargs):
    if instance.user:
        existing_image = platforms.objects.get(user=instance.user)
        if instance.image and existing_image.image != instance.image:
            existing_image.image.delete(False) 

# @receiver(pre_save, sender=platforms)
# def delete_old_image(sender, instance, *args, **kwargs):
#     if instance.id:
#         existing_image = platforms.objects.get(id=instance.id)
#         if instance.image and existing_image.image != instance.image:
#             existing_image.image.delete(False)    

# @receiver(post_delete, sender=platforms)
# def delete_old_image_when_del(sender, instance, *args, **kwargs):
#     if instance.id:
#         existing_image = platforms.objects.get(id=instance.id)
#         if instance.image and existing_image.image != instance.image:
#             existing_image.image.delete(False)                    
                          

class data(models.Model):
    isDirectOn=models.BooleanField(default=False)
    index_num=models.CharField(max_length=200, null=True, blank=True)
    user_id=models.CharField(max_length=200, null=True, blank=True)
    form_id=models.CharField(max_length=200, null=True, blank=True)
    name =models.CharField(max_length=200, null=True, blank=True)
    isActive=models.BooleanField(default=False)
    title=models.CharField(max_length=200, null=True, blank=True)
    domain=models.CharField(max_length=200, null=True, blank=True)
    username=models.CharField(max_length=200, null=True, blank=True)
    color1=models.CharField(max_length=50 , blank=True, null=True,default="#0000FF")
    color2=models.CharField(max_length=50 , blank=True, null=True,default="#0000FF")
    image=models.FileField(blank=True)             

    def __str__(self):
        return str(self.user_id) + " " + str(self.name)

        
@receiver(pre_save, sender=data)
def delete_old_image_data(sender, instance, *args, **kwargs):
    if instance.user:
        existing_image = data.objects.get(user=instance.user)
        if instance.image and existing_image.image != instance.image:
            existing_image.image.delete(False) 
                   
                          



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




############################################ custom page #######################################################
class title(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    text=models.CharField(max_length=200, null=True, blank=True)
    fontSize=models.CharField(max_length=200, null=True, blank=True)
    fontName=models.CharField(max_length=200, null=True, blank=True)
    fontType=models.CharField(max_length=200, null=True, blank=True)
    fontColor=models.CharField(max_length=200, null=True, blank=True)


class header(models.Model):
    user = models.ForeignKey(User,unique=False , on_delete=models.CASCADE)
    text=models.TextField(blank=True)
    fontSize=models.CharField(max_length=200, null=True, blank=True)
    fontName=models.CharField(max_length=200, null=True, blank=True)
    fontType=models.CharField(max_length=200, null=True, blank=True)
    fontColor=models.CharField(max_length=200, null=True, blank=True)    


class product(models.Model):
    user=models.ForeignKey(User,unique=False , on_delete=models.CASCADE)
    name=models.CharField(max_length=200, null=True, blank=True)
    image1=models.ImageField(null=True, blank=True)
    image2=models.ImageField(null=True, blank=True)
    image3=models.ImageField(null=True, blank=True)
    image4=models.ImageField(null=True, blank=True)
    image5=models.ImageField(null=True, blank=True)
    price=models.CharField(max_length=200, null=True, blank=True)
    description =models.TextField(blank=True)
    discount =models.CharField(max_length=200, null=True, blank=True)
    payment=models.CharField(max_length=200, null=True, blank=True)
    connection=models.CharField(max_length=200, null=True, blank=True)
    report=models.CharField(max_length=200, null=True, blank=True)
    info=models.CharField(max_length=200, null=True, blank=True)

@receiver(pre_save, sender=product)
def delete_old_image_product(sender, instance, *args, **kwargs):
    if instance.user:
        existing_image = product.objects.get(user=instance.user)
        if instance.image1 and existing_image.image1 != instance.image1:
            existing_image.image1.delete(False) 

        if instance.image2 and existing_image.image2 != instance.image2:
            existing_image.image2.delete(False)

        if instance.image3 and existing_image.image3 != instance.image3:
            existing_image.image3.delete(False)           
        if instance.image4 and existing_image.image4 != instance.image4:
            existing_image.image1.delete(False)    
        if instance.image5 and existing_image.image5 != instance.image5:
            existing_image.image5.delete(False)    


class html(models.Model) :
    user=models.ForeignKey(User,unique=False , on_delete=models.CASCADE)
    body =   models.TextField(blank=True)
    info=models.CharField(max_length=200, null=True, blank=True)


class contact_form    (models.Model) :
    user=models.ForeignKey(User,unique=False , on_delete=models.CASCADE)
    subject=models.CharField(max_length=200, null=True, blank=True)
    content=models.TextField(blank=True)
    From=models.CharField(max_length=200, null=True, blank=True)
    to=models.CharField(max_length=200, null=True, blank=True)



class RSS_Feed(models.Model) :
    user=models.ForeignKey(User,unique=False , on_delete=models.CASCADE)
    rss_feed=models.CharField(max_length=200, null=True, blank=True)



class Link(models.Model )  :
    user=models.ForeignKey(User,unique=False , on_delete=models.CASCADE)
    image=models.ImageField(null=True, blank=True)
    link=models.CharField(max_length=200, null=True, blank=True)
    color=models.CharField(max_length=200, null=True, blank=True)

@receiver(pre_save, sender=Link)
def delete_old_image_Link(sender, instance, *args, **kwargs):
    if instance.user:
        existing_image = Link.objects.get(user=instance.user)
        if instance.image and existing_image.image != instance.image:
            existing_image.image.delete(False)     


class IMAGE(models.Model):
    user=models.ForeignKey(User,unique=False , on_delete=models.CASCADE)
    image=models.ImageField(null=True, blank=True)

@receiver(pre_save, sender=IMAGE)
def delete_old_image_IMAGE(sender, instance, *args, **kwargs):
    if instance.user:
        existing_image = IMAGE.objects.get(user=instance.user)
        if instance.image and existing_image.image != instance.image:
            existing_image.image.delete(False)      