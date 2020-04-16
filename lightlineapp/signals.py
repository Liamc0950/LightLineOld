from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User, CueList, Project


@receiver(post_save, sender=Project)
def createProject(sender, instance, created, **kwargs):
    if instance and created:
        CueList.objects.create(listName="Main Cue List (" + str(instance.showNameShort) + ")", project=instance, active=True)