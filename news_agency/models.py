from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField()
    bio = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    instagram = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.username


class Newspaper(models.Model):
    title = models.CharField(max_length=63, unique=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    topics = models.ManyToManyField(Topic, related_name="newspapers")
    publishers = models.ManyToManyField(Redactor, related_name="newspapers")

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-published_date"]
