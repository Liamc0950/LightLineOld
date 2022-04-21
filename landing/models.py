from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # There is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.

    id = models.AutoField(primary_key=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.URLField(blank=True)

    # A timestamp representing when this object was created.
    created = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    lastUpdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def getName(self):
        return self.user.first_name + " " + self.user.last_name

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
