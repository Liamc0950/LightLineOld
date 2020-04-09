# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Color(models.Model):
    lastUpdate = models.DateTimeField(auto_now=True)
    colorName = models.CharField(max_length = 32)
    colorCode = models.CharField(max_length = 16)
    colorHex = models.CharField(max_length = 32, default="0xFFFFFFFF")

    def __str__(self):
        return self.colorCode


class ColorFlag(models.Model):
    lastUpdate = models.DateTimeField(auto_now=True)
    color1 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color1')
    color2 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color2', default='NC')
    index = models.IntegerField(default=1)

    def __str__(self):
        return str(self.color1) + " " + str(self.color2)

class Followspot(models.Model):
    lastUpdate = models.DateTimeField(auto_now=True)
    spotType = models.CharField(max_length = 32)
    wattage = models.IntegerField(default=255)

    def __str__(self):
        return self.spotType


class Operator(models.Model):
    lastUpdate = models.DateTimeField(auto_now=True)
    operatorNumber = models.IntegerField(default=1)
    operatorName = models.CharField(max_length=64)
    followspotType = models.ForeignKey(Followspot, on_delete=models.CASCADE)
    notes = models.CharField(max_length=512)

    def __str__(self):
        return self.operatorName


class Focus(models.Model):
    lastUpdate = models.DateTimeField(auto_now=True)
    focusDescr = models.CharField(max_length=32)
    
    def __str__(self):
        return self.focusDescr


class Shot(models.Model):
    lastUpdate = models.DateTimeField(auto_now=True)
    shotDescr = models.CharField(max_length=32)
    
    def __str__(self):
        return self.shotDescr


class SpotCue(models.Model):
    lastUpdate = models.DateTimeField(auto_now=True)
    cueLabel = models.CharField(max_length = 100)
    pageNumber = models.IntegerField(default=1)
    eosCueNumber = models.IntegerField(default=1)

    def __str__(self):
        return self.cueLabel

    #Return array of Actions that have this spot cue as their cue field
    def getActions(self):
        return Action.objects.filter(cue=self)


class Action(models.Model):
    lastUpdate = models.DateTimeField(auto_now=True)
    fadeTime = models.IntegerField(default=3)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    colorFlag = models.ForeignKey(ColorFlag, on_delete=models.CASCADE)
    focus = models.ForeignKey(Focus, on_delete=models.CASCADE)
    shotType = models.ForeignKey(Shot, on_delete=models.CASCADE)
    cue = models.ForeignKey(SpotCue, default=1, on_delete=models.CASCADE)
    intensity = models.IntegerField(default=100)


    def __str__(self):
        return str(self.focus) + " " + str(self.shotType) + " " + str(self.fadeTime)

    def getColorOne(self):
        

        return self.colorFlag.color1

    def getColorTwo(self):
        return self.colorFlag.color2
    """
    def getColorFlagClass(self):
        opActions = Action.objects.filter(operator=self.operator)
        lastAction = Action.objects.filter(operator=self.operator).filter(cue.eosCueNumber<self.cue.eosCueNumber).order_by('eosCueNumber')[:2]
        if lastAction[0].colorFlag == self.colorFlag and lastAction[1].colorFlag == self.colorFlag:
            return ""
        elif lastAction[0].colorFlag != self.colorFlag:
            return "hotChange"
        elif lastAction[1].colorFlag != self.colorFlag:
            return "darkChange"
    """
    
    def getFocusClass(self):
        return
    
    def getShotTypeClass(self):
        return

    def getIntensityTypeClass(self):
        return
