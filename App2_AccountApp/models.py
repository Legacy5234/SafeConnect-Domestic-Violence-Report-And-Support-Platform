from django.db import models
from django.templatetags.static import static
from django.contrib.auth.models import  User

# Create your models here.
#---------------------------------------------------------------------------------------------------------
# USER PROFILE MODEL CLASS
#---------------------------------------------------------------------------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    email = models.EmailField(unique=True, null=False)  
    location = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def profile_image(self):
        if self.image:
            return self.image.url
        return static('images/avatar_default.svg')

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.user.username
