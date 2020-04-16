# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from myapp.models import Action, ShotCue, Operator

class AnimalTestCase(TestCase):
    def setUp(self):
        cue = ShotCue.objects.create(eosCueNumber=1)
        op = Operator.objects.create(operatorName = "test")
        Action.objects.create(operator = op, cue = cue)

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
