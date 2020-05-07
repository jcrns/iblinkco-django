from django.contrib import admin

from .models import JobPost, Milestone ,MilestoneFiles

admin.site.register(JobPost)
admin.site.register(Milestone)
admin.site.register(MilestoneFiles)
