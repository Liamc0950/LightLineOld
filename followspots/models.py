# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Followspot(models.Model):
    spotType = models.CharField(max_length = 32)
    wattage = models.IntegerField(default=255)

class Color(models.Model):
    colorName = models.CharField(max_length = 32)
    colorCode = models.CharField(max_length = 16)
    colorRed = models.IntegerField(default=255)
    colorGreen = models.IntegerField(default=255)
    colorBlue = models.IntegerField(default=255)

class Operator(models.Model):
    operatorNumber = models.IntegerField(default=1)
    operatorName = models.CharField(max_length=64)
    followspotType = models.ForeignKey(Followspot)
    notes = models.CharField(max_length=512)

class Focus(models.Model):
    focusDescr = models.CharField(max_length=32)

class Shot(models.Model):
    shotDescr = models.CharField(max_length=32)

class SpotCue(models.Model):
    cueLabel = models.CharField(max_length = 100)
    pageNumber = models.IntegerField(default=1)
    eosCueNumber = models.IntegerField(default=1)
    lastUpdate = models.DateTimeField('Last updated')
    fadeTime = models.IntegerField(default=3)
    color = models.ForeignKey(Color)

class Action(models.Model):
    lastUpdate = models.DateTimeField('Last updated')
    fadeTime = models.IntegerField(default=3)
    color = models.ForeignKey(Color)
    operator = models.ForeignKey(Operator)
    focus = models.ForeignKey(Focus)
    shotType = models.ForeignKey(Shot)
