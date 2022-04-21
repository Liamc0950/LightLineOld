from django.db import models

from database.models import Color
from projectManager.models import Project
from cueList.models import Cue

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