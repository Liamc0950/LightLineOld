from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from landing.models import Profile
from django.utils import timezone
from .views import *

from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse

from django.db import IntegrityError


# models test
class NotesTest(TestCase):

    def create_workNote(self, text="only a test"):
        user = User.objects.create_user(username='dsa', password='12345')
        profile = Profile.objects.get(user=user)
        projectActive = Project.objects.create(showName="test show", showNameShort="ts", lightingDesigner=profile, active=True)
        return WorkNote.objects.create(noteText=text, createdBy=profile, project=projectActive)

    def test_workNote_creation(self):
        note = self.create_workNote()
        self.assertTrue(isinstance(note, WorkNote))
        self.assertEqual(note.__str__(), note.noteText)

class NotesIndexViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        user = User.objects.create_user(username='user', password='user')
        profile = Profile.objects.get(user=user)
        projectActive = Project.objects.create(showName="test show", showNameShort="ts", lightingDesigner=profile, active=True)
        cueListActive = CueList.objects.create(listName="test cuelist", project=projectActive, active=True)

        self.client.login(username='user', password='user')


    def test_no_workNotes(self):
        """
        If no workNotes exist, no context is sent
        """
        #LOG IN
        self.client.login(username='dsa', password='12345')
        response = self.client.get(reverse('notes_index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['workNotes'], [])

