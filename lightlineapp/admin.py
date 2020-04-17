# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *

admin.site.register(Cue)
admin.site.register(Action)
admin.site.register(Color)
admin.site.register(Followspot)
admin.site.register(Operator)
admin.site.register(Focus)
admin.site.register(Shot)
admin.site.register(ColorFlag)
admin.site.register(CueList)
admin.site.register(Project)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
