# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Followspot(models.Model):
    spotType = models.CharField(max_length = 32)
    wattage = models.IntegerField(default=255)

    def __str__(self):
        return self.spotType

class Color(models.Model):
    colorName = models.CharField(max_length = 32)
    colorCode = models.CharField(max_length = 16)
    colorHex = models.CharField(max_length = 32, default="0xFFFFFFFF")

    def __str__(self):
        return self.colorCode

class Operator(models.Model):
    operatorNumber = models.IntegerField(default=1)
    operatorName = models.CharField(max_length=64)
    followspotType = models.ForeignKey(Followspot)
    notes = models.CharField(max_length=512)

    def __str__(self):
        return self.operatorName


class Focus(models.Model):
    focusDescr = models.CharField(max_length=32)
    
    def __str__(self):
        return self.focusDescr


class Shot(models.Model):
    shotDescr = models.CharField(max_length=32)
    
    def __str__(self):
        return self.shotDescr


class SpotCue(models.Model):
    cueLabel = models.CharField(max_length = 100)
    pageNumber = models.IntegerField(default=1)
    eosCueNumber = models.IntegerField(default=1)
    lastUpdate = models.DateTimeField('Last updated')

    def __str__(self):
        return self.cueLabel

    def getActions(self):
        return Action.objects.filter(cue=self)


class Action(models.Model):
    lastUpdate = models.DateTimeField('Last updated')
    fadeTime = models.IntegerField(default=3)
    color = models.ForeignKey(Color)
    operator = models.ForeignKey(Operator)
    focus = models.ForeignKey(Focus)
    shotType = models.ForeignKey(Shot)
    cue = models.ForeignKey(SpotCue, default=1)
    intensity = models.IntegerField(default=100)


    def __str__(self):
        return str(self.focus) + " " + str(self.shotType) + " " + str(self.fadeTime)
