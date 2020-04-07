# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(SpotCue)
admin.site.register(Action)
admin.site.register(Color)
admin.site.register(Followspot)
admin.site.register(Operator)
admin.site.register(Focus)
admin.site.register(Shot)
admin.site.register(ColorFlag)