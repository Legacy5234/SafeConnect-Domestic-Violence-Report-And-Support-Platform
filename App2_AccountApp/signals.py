from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from . models import Profile

# Profile creation when a new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        Profile.objects.create (
            user = user,
            email = user.email
        )
        #Enabling admin to change email address on the user and reflecting it on the profile of the user
    else:
        profile = get_object_or_404(Profile, user=user)
        profile.email = user.email
        profile.save()


# User table update when user update profile section
@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    profile = instance
    if created == False:
        user = get_object_or_404(User, id=profile.user.id)

        # Adding a conditional to break the infinite loop
        if user.email != profile.email:
            user.email = profile.email
            user.save()