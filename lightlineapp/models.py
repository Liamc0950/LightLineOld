# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


#Regex for csv parsing
import re



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

#Project - Defines the 
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    #Name of show
    showName = models.CharField(max_length = 64)
    showNameShort = models.CharField(max_length = 32, default="")

    #Profile that the project is tied to
    #The Profile's name will also be used to populate paperwork with Lighting Designer
    lightingDesigner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    #Will have many-to-many Profile relationship with Shared Users - may need custom through table to define roles?

    #If true, database, cueList, Followspot and notes views will display data from this project
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.showName



class Breakout(models.Model):
    id = models.AutoField(primary_key=True)
    circuitLabel = models.CharField(max_length = 32, unique=True)
    service = models.IntegerField()

class Circuit(models.Model):
    id = models.AutoField(primary_key=True)
    circuitLabel = models.CharField(max_length = 32, unique=True)
    service = models.IntegerField()
    breakout = models.ForeignKey(Breakout, on_delete=models.CASCADE)


class CableType(models.Model):
    id = models.AutoField(primary_key=True)
    cableTypeName = models.CharField(max_length = 32, unique=True)
    weightPerFoot = models.IntegerField()
    ampRating = models.IntegerField()
    power = models.BooleanField(default=False)
    data = models.BooleanField(default=False)

class Cable(models.Model):
    id = models.AutoField(primary_key=True)
    cableLabel = models.CharField(max_length = 32, unique=True)
    cableType = models.CharField(max_length = 16, unique=True)
    cableLength = models.IntegerField()
    weight = models.IntegerField()


class Gobo(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    goboName = models.CharField(max_length = 32)
    goboCode = models.CharField(max_length = 16, unique=True)
    imageUrl = models.CharField(max_length = 128)

    def __str__(self):
        return self.goboCode


#Defines a Color filter model
class Color(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    
    #Prose name, Numerical code, and hex color code for displaying swatch
    colorName = models.CharField(max_length = 32)
    colorCode = models.CharField(max_length = 16, unique=True)
    colorHex = models.CharField(max_length = 32, default="0xFFFFFFFF")

    def __str__(self):
        return self.colorCode

    # #Get the Color instance matching the provided name
    # def getColor(self, name):
    #     try:
    #         return Color.objects.get(colorName = name)
    #     except:
    #         return None


class Accessory(models.Model):
    id = models.AutoField(primary_key=True)
    accessoryName = models.CharField(max_length = 32, unique=True)
    weight = models.IntegerField()

class FocusChart(models.Model):
    id = models.AutoField(primary_key=True)
    chartLabel = models.CharField(max_length = 32, unique=False)


class FocusNote(models.Model):
    id = models.AutoField(primary_key=True)
    noteLabel = models.CharField(max_length = 32, unique=False)

class WorkNote(models.Model):
    id = models.AutoField(primary_key=True)
    noteLabel = models.CharField(max_length = 32, unique=False)


class Position(models.Model):
    id = models.AutoField(primary_key=True)
    positionName = models.CharField(max_length = 32, unique=True)

    def __str__(self):
        return self.positionName


class InstrumentType(models.Model):
    id = models.AutoField(primary_key=True)
    typeName = models.CharField(max_length = 64)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    load = models.IntegerField(blank=True, null=True)
    beamAngle = models.IntegerField(blank=True, null=True)
    fieldAngle = models.IntegerField(blank=True, null=True)
    zoomAngleMin = models.IntegerField(blank=True, null=True)
    zoomAngleMax = models.IntegerField(blank=True, null=True)
    zoomAble = models.BooleanField(default=False, blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.typeName

#Defines a Lighting Instrument
class Instrument(models.Model):
    id = models.AutoField(primary_key=True)
    #Project that this instrument is associated with - this instrument instance will only be associated with one project
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    #Instrument Type - Instrument types are local to projects, but many instruments can share type
    instrumentType = models.ForeignKey(InstrumentType, on_delete=models.CASCADE, blank=True, null=True)
    #Position - Positions are local to projects, but many instruments can share position
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    unitNumber = models.IntegerField()
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, blank=True, null=True)
    color = models.ManyToManyField(Color, related_name="colors", blank=True)
    gobo = models.ForeignKey(Gobo, on_delete=models.CASCADE, blank=True, null=True)
    goboSize = models.CharField(max_length = 8, unique=False, blank=True, null=True)
    purpose = models.CharField(max_length = 128)
    dimmer = models.IntegerField(blank=True, null=True)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, blank=True, null=True)
    breakout = models.ForeignKey(Breakout, on_delete=models.CASCADE, blank=True, null=True)
    dimmerPhase = models.CharField(max_length = 8, unique=False, blank=True, null=True)
    address = models.IntegerField(blank=True, null=True)
    universe = models.IntegerField(blank=True, null=True)
    channel = models.IntegerField(blank=True, null=True)
    focusChart = models.ForeignKey(FocusChart, on_delete=models.CASCADE, blank=True, null=True)
    cable = models.ForeignKey(Cable, on_delete=models.CASCADE, blank=True, null=True)
    focusNote = models.ForeignKey(FocusNote, on_delete=models.CASCADE, blank=True, null=True)
    workNote = models.ForeignKey(WorkNote, on_delete=models.CASCADE, blank=True, null=True)

    #Return all colors associated with this Instrument
    def getColors(self):
        return self.color.all()

    def __str__(self):
        return str(self.instrumentType) + " CHANNEL " + str(self.channel)

    #Add Instrument instanced from a csv file exported from LightWright 6
    def addInstrumentsFromCSV(csv, activeProject):
        for line in csv:
            line =  line.split(',')

            if len(line[0]) == 1 or line[0] == "Purpose":
                pass
            else: 
                instrument = Instrument()
                #PROJECT
                instrument.project = activeProject
                #PURPOSE
                instrument.purpose = line[0]
                #CHANNEL
                if line[1] != '':
                    chan = line[1]
                    chan = re.search('\(([^)]+)', chan).group(1)
                    instrument.channel = chan
                #DIMMER
                if line[2] != '':
                    instrument.dimmer = line[2]
                else:
                    pass
                #ADDRESS - need to parse out universe
                # if line[3] != '':
                #     instrument.address = line [3]
                # else:
                #     pass
                #POSITION
                try:
                    instrument.position = Position.objects.get(positionName = line[4])
                except:
                    newPosition = Position()
                    newPosition.positionName = line[4]
                    newPosition.save()
                    instrument.position = newPosition

                #UNIT #
                if line[4] != '':
                    instrument.unitNumber = line[5]
                else:
                    pass
                #INSTRUMENT TYPE
                try:
                    instrument.instrumentType =  InstrumentType.objects.get(typeName = line[6])
                except:
                    newType = InstrumentType()
                    newType.typeName = line[6]
                    if line[7] != '':
                        loadInt = int(re.sub("w", " ", line[7]))
                        newType.load = loadInt
                    else:
                        pass
                    newType.project = activeProject
                    newType.save()
                    instrument.instrumentType = newType

                #LOAD
                # if line[7] != '':
                #     instrument.instrumentType.load = line[7]
                # else:
                #     pass
                #ACCESSORY
                # if Accessory.objects.get(accessoryName = line[8]):
                #     instrument.position = Position.objects.get(accessoryName = line[8])
                # else:
                #     newAccessory = Accessory()
                #     newAccessory.accessoryName = line[8]
                #     instrument.accessory = newAccessory
                #COLOR
                colorString = line[9]
                
                colorSplit = colorString.split(" ")

                #SAVE TO ALLOW MANY TO MANY
                instrument.save()

                for name in colorSplit:
                    try:
                        instrument.color.add(Color.objects.get(colorCode = name))
                        print("FOUND " + name)

                    except:
                        print("NOT FOUND " + name)
                        pass


                #GOBO

                goboString = line[10]
                
                #SPLIT THE STRING, WE SHOULD ONLY LOOK AT THE FIRST SET OF CHARACTERS BEFORE A SPACE, IF A SPACE EXISTS
                goboSplit = goboString.split(" ")


                for name in goboSplit:
                    try:
                        instrument.gobo = (Gobo.objects.get(goboCode = name))
                        print("FOUND " + name)

                    except:
                        print("NOT FOUND " + name)
                        pass


                #SAVE INSTRUMENT
                instrument.save()  


class CueList(models.Model):
    id = models.AutoField(primary_key=True)
    listName = models.CharField(max_length = 64)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    cueListNumber = models.IntegerField(default=1)
    active = models.BooleanField(default=False)


    def __str__(self):
        return self.listName

    def getLastCue(self):
        cuesInList = Cue.objects.order_by('eosCueNumber').filter(cueList=self)
        try:
            lastCue= cuesInList[len(cuesInList) - 1]
            return lastCue.eosCueNumber
        except:
            return 0




class ColorFlag(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    color1 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color1')
    index = models.IntegerField(default=1)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.color1)


class Followspot(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    spotType = models.CharField(max_length = 32)
    wattage = models.IntegerField(default=3000)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    available = models.IntegerField(default=1)
    dimmerControlled = models.BooleanField(default= False)


    def __str__(self):
        return self.spotType


class Operator(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    operatorNumber = models.IntegerField(default=1)
    operatorName = models.CharField(max_length=64)
    followspotType = models.ForeignKey(Followspot, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    #Bridge between host user and shared user
    #shareNode = models.ForeignKey(ShareNode, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.operatorName


class Focus(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    focusDescr = models.CharField(max_length=32, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.focusDescr


class Shot(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    shotDescr = models.CharField(max_length=32)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.shotDescr

class CueManager(models.Manager):
    def createNext(self, lastCueNum):

        increment = 2

        cue = self.create(eosCueNumber= lastCueNum + increment)
        # do something with the book
        return cue


class Cue(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    cueLabel = models.CharField(max_length = 100, default="", blank=True)
    pageNumber = models.IntegerField(default=1)
    eosCueNumber = models.IntegerField(default=1)
    cueTime = models.IntegerField(default=5)
    cueDescription = models.CharField(max_length = 100, default="", blank=True)
    cueList = models.ForeignKey(CueList, on_delete=models.CASCADE, default=1)

    # block = models.BooleanField(default=False)

    objects = CueManager()


    def __str__(self):
        return self.cueLabel


    #Return array of Actions that have this spot cue as their cue field
    def getActions(self):
        try:
            return Action.objects.filter(cue=self)
        except:
            None

    #Return Header for cue if exists
    def getHeader(self):
        try:
            return Header.objects.get(cue=self)
        except:
            return None
    


class Header(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    cue = models.ForeignKey(Cue, default=1, on_delete=models.CASCADE)
    headerTitle = models.CharField(max_length = 100, default="", blank=True)
    cueList = models.ForeignKey(CueList, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.headerTitle


class Action(models.Model):
    id = models.AutoField(primary_key=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    fadeTime = models.IntegerField(default=3)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    colorFlag = models.ForeignKey(ColorFlag, on_delete=models.CASCADE, default=1)
    focus = models.ForeignKey(Focus, on_delete=models.CASCADE)
    shotType = models.ForeignKey(Shot, on_delete=models.CASCADE)
    cue = models.ForeignKey(Cue, default=1, on_delete=models.CASCADE)
    intensity = models.IntegerField(default=100)

    def __str__(self):
        return str(self.cue.eosCueNumber) + " " + str(self.focus) + " " + str(self.shotType) + " " + str(self.fadeTime)

    #return the eosCueNumber
    def getCueNumber(self):
        return self.cue.eosCueNumber

    #Return the first Color in the color flag
    def getColorOne(self):
        return self.colorFlag.color1

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
        
        #if the colorFlag of the last action is the same as in this action, return noChange
        if lastAction.colorFlag == self.colorFlag:
            return "noChange"
        #if the colorFlag of the last action is different, and the last action's intensity is not 0, return "hotChange"
        elif lastAction.colorFlag != self.colorFlag and lastAction.intensity != 0:
            return "hotChange"
        #if the colorFlag of the last action is different, and the last action's intensity is 0, return "darkChange"
        elif lastAction.colorFlag != self.colorFlag and lastAction.intensity == 0:
            return "darkChange"
        #if the colorFlag of the action two back was different, and the intensity of the last action was 0, return "darkChange"
        elif secondLastAction.colorFlag != self.colorFlag and lastAction.intensity == 0:
            return "darkChange"
        #if the colorFlag of the action two back was different, and the intensity of the last action was not 0, return "darkChange"
        elif secondLastAction.colorFlag != self.colorFlag and lastAction.intensity != 0:
            return "hotChange"

 
    #Returns the proper color coding class as a string
    #If the focus is different in this operator's last action, return hotChange, if a dark change occurred return "darkChange", 
    #and if a hot change occurred return "hotChange"  
    def getFocusClass(self):
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
            if lastAction.focus == self.focus:
                return "noChange"
            #if the colorFlag of the last action is different than this action, and the intensity
            # of the last action is 0, return darkChange
            elif lastAction.focus != self.focus and lastAction.intensity == 0:
                return "darkChange"

            #if the colorFlag of the last action is different, and the last action's intensity is not 0, return "hotChange"
            elif lastAction.focus != self.focus and lastAction.intensity != 0:
                return "hotChange"
        
        #if the focus of the last action is the same as in this action, return noChange
        if lastAction.focus == self.focus:
            return "noChange"
        #if the focus of the last action is different, and the last action's intensity is not 0, return "hotChange"
        elif lastAction.focus != self.focus and lastAction.intensity != 0:
            return "hotChange"
        #if the focus of the last action is different, and the last action's intensity is 0, return "darkChange"
        elif lastAction.focus != self.focus and lastAction.intensity == 0:
            return "darkChange"
        #if the focus of the action two back was different, and the intensity of the last action was 0, return "darkChange"
        elif secondLastAction.focus != self.focus and lastAction.intensity == 0:
            return "darkChange"
        #if the focus of the action two back was different, and the intensity of the last action was not 0, return "darkChange"
        elif secondLastAction.focus != self.focus and lastAction.intensity != 0:
            return "hotChange"

 
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