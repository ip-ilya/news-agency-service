from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField()

    def __str__(self) -> str:
        return self.username


class Newspaper(models.Model):
    title = models.CharField(max_length=63)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="newspapers"
    )
    publishers = models.ManyToManyField(
        Redactor,
        related_name="newspapers"
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-published_date"]
