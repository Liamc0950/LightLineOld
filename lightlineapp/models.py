# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # There is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.


    #Setup options for user roles. These will help to determine permissions
    LD = 1
    ASSISTANT = 2
    ASSOCIATE = 3
    ME = 4
    ELECTRICIAN= 5
    FOLLOWSPOT_OP = 6
    STAGE_MANAGER = 7
    ROLE_CHOICES = (
        (LD, 'Lighting Designer'),
        (ASSISTANT, 'Assistant'),
        (ASSOCIATE, 'Associate'),
        (ME, 'Master Electrician'),
        (ELECTRICIAN, 'Electrician'),
        (FOLLOWSPOT_OP, 'Followspot Operator'),
        (STAGE_MANAGER, 'Stage Manager'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    image = models.URLField(blank=True)

    # A timestamp representing when this object was created.
    created = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    lastUpdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    showName = models.CharField(max_length = 64)
    showNameShort = models.CharField(max_length = 32, default="")

    lightingDesigner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.showName


class CueList(models.Model):
    id = models.AutoField(primary_key=True)
    listName = models.CharField(max_length = 64)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.listName


class Color(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    colorName = models.CharField(max_length = 32)
    colorCode = models.CharField(max_length = 16)
    colorHex = models.CharField(max_length = 32, default="0xFFFFFFFF")

    def __str__(self):
        return self.colorCode


class ColorFlag(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    color1 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color1')
    color2 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color2', default='NC')
    index = models.IntegerField(default=1)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.color1) + " " + str(self.color2)

class Followspot(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    spotType = models.CharField(max_length = 32)
    wattage = models.IntegerField(default=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.spotType


class Operator(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    operatorNumber = models.IntegerField(default=1)
    operatorName = models.CharField(max_length=64)
    followspotType = models.ForeignKey(Followspot, on_delete=models.CASCADE)
    notes = models.CharField(max_length=512)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.operatorName


class Focus(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    focusDescr = models.CharField(max_length=32)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.focusDescr


class Shot(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    shotDescr = models.CharField(max_length=32)

    def __str__(self):
        return self.shotDescr


class SpotCue(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    cueLabel = models.CharField(max_length = 100)
    pageNumber = models.IntegerField(default=1)
    eosCueNumber = models.IntegerField(default=1)
    cueList = models.ForeignKey(CueList, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.cueLabel

    #Return array of Actions that have this spot cue as their cue field
    def getActions(self):
        return Action.objects.filter(cue=self)


class Action(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    fadeTime = models.IntegerField(default=3)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    colorFlag = models.ForeignKey(ColorFlag, on_delete=models.CASCADE)
    focus = models.ForeignKey(Focus, on_delete=models.CASCADE)
    shotType = models.ForeignKey(Shot, on_delete=models.CASCADE)
    cue = models.ForeignKey(SpotCue, default=1, on_delete=models.CASCADE)
    intensity = models.IntegerField(default=100)

    def __str__(self):
        return str(self.cue.eosCueNumber) + " " + str(self.focus) + " " + str(self.shotType) + " " + str(self.fadeTime)

    #return the eosCueNumber
    def getCueNumber(self):
        return self.cue.eosCueNumber

    #Return the first Color in the color flag
    def getColorOne(self):
        return self.colorFlag.color1
    #Return the second Color in the color flag
    def getColorTwo(self):
        return self.colorFlag.color2

    #Returns the proper color coding class as a string
    #If the color flag is different in this operator's last action, return hotChange, if a dark change occurred return "darkChange", 
    #and if a hot change occurred return "hotChange"  
    def getColorFlagClass(self):
        #get all the actions assigned to this operator
        opActions = Action.objects.filter(operator=self.operator)
        #sort actions in descending order - so more recent actions are first
        sortedActions = opActions.order_by('-cue__eosCueNumber')
        #remove any actions that take place after the current action
        filteredActions = sortedActions.filter(cue__eosCueNumber__lte =  self.getCueNumber())
        #remove the current action
        filteredActions = filteredActions.exclude(id=self.id)
        #get the last action before current
        print("CURRENT ACTION")
        print(self)
        print("PAST ACTIONS")
        print(filteredActions)
        try:
            lastAction = filteredActions[0]
        except IndexError:
            return "noChange"
            
        #get the action two before current
        try:
            secondLastAction = filteredActions[1]
        except IndexError:
            #if the colorFlag of the last action is the same as in this action, return noChange
            if lastAction.colorFlag == self.colorFlag:
                return "noChange"
            #if the colorFlag of the last action is different than this action, and the intensity
            # of the last action is 0, return darkChange
            elif lastAction.colorFlag != self.colorFlag and lastAction.intensity == 0:
                return "darkChange"

            #if the colorFlag of the last action is different, and the last action's intensity is not 0, return "hotChange"
            elif lastAction.colorFlag != self.colorFlag and lastAction.intensity != 0:
                return "hotChange"
        
        #if the colorFlag of the last action, and the action before, are the same as in this action, return noChange
        if lastAction.colorFlag == self.colorFlag and secondLastAction.colorFlag == self.colorFlag:
            return "noChange"
        #if the colorFlag of the last action is different, and the last action's intensity is not 0, return "hotChange"
        elif lastAction.colorFlag != self.colorFlag and lastAction.intensity != 0:
            return "hotChange"
        #if the colorFlag of the action two back was different, and the intensity of the last action was 0, return "darkChange"
        elif secondLastAction.colorFlag != self.colorFlag and lastAction.intensity == 0:
            return "darkChange"
 
    #Returns the proper color coding class as a string
    #If the focus is different in this operator's last action, return hotChange, if a dark change occurred return "darkChange", 
    #and if a hot change occurred return "hotChange"  
    def getFocusClass(self):
        return "noChange"
 
    #Returns the proper color coding class as a string
    def getShotTypeClass(self):
        #get all the actions assigned to this operator
        opActions = Action.objects.filter(operator=self.operator)
        #sort actions in descending order - so more recent actions are first
        sortedActions = opActions.order_by('cue__eosCueNumber')
        #remove any actions that take place after the current action
        filteredActions = sortedActions.filter(cue__eosCueNumber__lt =  self.getCueNumber())
        #remove the current action
        filteredActions = filteredActions.exclude(id=self.id)

        #get the last action before current. If list is empty, return noChange as this must be 
        #this operator's first action in the cue list
        try:
            lastAction = filteredActions[0]
        except IndexError:
            return "noChange"

        #If the intensity of the last action by this operator is not equal to the current intensity,
        #return easyChange
        if lastAction.shotType != self.shotType:
            return "easyChange"
        else:
            return "noChange"

    #Returns the proper color coding class as a string
    def getIntensityClass(self):
        #get all the actions assigned to this operator
        opActions = Action.objects.filter(operator=self.operator)
        #sort actions in descending order - so more recent actions are first
        sortedActions = opActions.order_by('cue__eosCueNumber')
        #remove any actions that take place after the current action
        filteredActions = sortedActions.filter(cue__eosCueNumber__lt =  self.getCueNumber())
        #remove the current action
        filteredActions = filteredActions.exclude(id=self.id)

        #get the last action before current. If list is empty, return noChange as this must be 
        #this operator's first action in the cue list
        try:
            lastAction = filteredActions[0]
        except IndexError:
            return "noChange"

        #If the intensity of the last action by this operator is not equal to the current intensity,
        #return easyChange
        if lastAction.intensity != self.intensity:
            return "easyChange"
        else:
            return "noChange"

    #Returns the proper color coding class as a string
    def getTimeClass(self):
        #get all the actions assigned to this operator
        opActions = Action.objects.filter(operator=self.operator)
        #sort actions in descending order - so more recent actions are first
        sortedActions = opActions.order_by('cue__eosCueNumber')
        #remove any actions that take place after the current action
        filteredActions = sortedActions.filter(cue__eosCueNumber__lt =  self.getCueNumber())
        #remove the current action
        filteredActions = filteredActions.exclude(id=self.id)

        #get the last action before current. If list is empty, return noChange as this must be 
        #this operator's first action in the cue list
        try:
            lastAction = filteredActions[0]
        except IndexError:
            return "noChange"

        #If the fadeTime of the last action by this operator is not equal to the current fadeTime,
        #return easyChange
        if lastAction.fadeTime != self.fadeTime:
            return "easyChange"
        else:
            return "noChange"