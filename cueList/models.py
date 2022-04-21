from django.db import models

from projectManager.models import Project



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
