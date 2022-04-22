from django.db import models

from database.models import *
from projectManager.models import Project
from landing.models import Profile

FIELD_CHOICES = (
    ('Instrument Type','INSTRUMENT_TYPE'),
    ('Position', 'POSITION'),
    ('Unit Number','UNIT_NUMBER'),
    ('Accessory','ACCESSORY'),
    ('Color','COLOR'),
    ('Gobo','GOBO'),
    ('Gobo Size','GOBO_SIZE'),
    ('Purpose','PURPOSE'),
    ('Dimmer','DIMMER'),
    ('Circuit','CIRCUIT'),
    ('Breakout','BREAKOUT'),
    ('Dimmer Phase','DIMMER_PHASE'),
    ('Address','ADDRESS'),
    ('Universe','UNIVERSE'),
    ('Channel','CHANNEL'),

)

class Note(models.Model):
    id = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    #Note text
    noteText = models.CharField(max_length=256)
    #Project that this note is associated with - this note instance will only be associated with one project
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    #Profile of user who created this note
    createdBy = models.ForeignKey(Profile, related_name="createdBy", on_delete=models.CASCADE)
    #Profile of user this note is assigned to
    assignedTo = models.ForeignKey(Profile, related_name="assignedTo", on_delete=models.CASCADE, blank=True, null=True)
    #Profile of the user who last updated this note
    lastUpdatedBy = models.ForeignKey(Profile, related_name="lastUpdatedBy", on_delete=models.CASCADE, blank=True, null=True)

    #PRIORITY
    priority = models.IntegerField(default=5)

    class Meta:
        abstract = True

    def __str__(self):
        return self.noteText


class WorkNote(Note):
    home_group = models.CharField(max_length=5)
    channelList = models.CharField(max_length=5)
    changeFieldSelection = models.CharField(max_length=16, choices=FIELD_CHOICES, default='INSTRUMENT_TYPE')
    #THESE FIELD WILL BE MADE AVAILABLE TO USER BASED ON THEIR SELECTION IN changeFieldSelection
    newInstrumentType = models.ForeignKey(InstrumentType, on_delete=models.CASCADE, blank=True, null=True)
    newPosition = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    newUnitNumber = models.IntegerField(blank=True, null=True)
    newAccessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, blank=True, null=True)
    newColor = models.ManyToManyField(Color, related_name="newColors", blank=True)
    newGobo = models.ForeignKey(Gobo, on_delete=models.CASCADE, blank=True, null=True)
    newGoboSize = models.CharField(max_length = 8, unique=False, blank=True, null=True)
    newPurpose = models.CharField(max_length = 128, blank=True, null=True)
    newDimmer = models.IntegerField(blank=True, null=True)
    newCircuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, blank=True, null=True)
    newBreakout = models.ForeignKey(Breakout, on_delete=models.CASCADE, blank=True, null=True)
    newDimmerPhase = models.CharField(max_length = 8, unique=False, blank=True, null=True)
    newAddress = models.IntegerField(blank=True, null=True)
    newUniverse = models.IntegerField(blank=True, null=True)
    newChannel = models.IntegerField(blank=True, null=True)

    
