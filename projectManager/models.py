from django.db import models

from landing.models import Profile

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
