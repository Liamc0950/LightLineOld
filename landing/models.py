from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.ImageField(default='default.jpg', upload_to='profile_images')

    # A timestamp representing when this object was created.
    created = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    lastUpdate = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return self.user.username

    def getName(self):
        return self.user.first_name + " " + self.user.last_name
