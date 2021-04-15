from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.core.validators import RegexValidator

# Create your models here

SOURCE_CHOICES= (
    ("Web","Web"),
    ('Friend','Friend'),
    ('Newsletter','Newsletter'),
    ('Email','Email')
)

CATEGORY_CHOICES=(
    ("Converted","Converted"),
    ("Contacted","Contacted"),
    ("Unconverted","Unconverted"),
)

class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    phone_regex = RegexValidator(regex=r'^\+1?\d{12}$', message="Phone number must be entered in the 12 digit format: '+999999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15,null=True, blank=True) # validators should be a list
    email= models.EmailField(max_length=254,null=True,blank=True)
    postal_code=models.IntegerField(null=True,blank=True)
    city = models.CharField(max_length=20,null=True,blank=True)
    country = models.CharField(max_length=20,null=True,blank=True)
    description=models.TextField(blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True,blank=True)
   

    source = models.CharField(choices=SOURCE_CHOICES,max_length=100)
    agent = models.ForeignKey("Agent",null=True, blank=True,on_delete=models.SET_NULL)
    organization = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    category= models.ForeignKey("Category", related_name="leads", on_delete=models.SET_NULL,null=True,blank=True)


    def __str__(self):
        return f"{self.f_name} {self.l_name}"

class Agent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) 
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email

class Category(models.Model):
    name = models.CharField(choices=CATEGORY_CHOICES,max_length=30,null=True,blank=True)
    organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


      
def org_create_trigger(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(org_create_trigger,sender=User)

