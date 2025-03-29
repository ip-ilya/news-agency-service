from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from news_agency.models import (
    Topic,
    Redactor,
    Newspaper
)


admin.site.unregister(Group)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    model = Topic


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    model = Redactor


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    model = Newspaper
