from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField("self", symmetrical=False)

    def __str__(self):
        return self.name


class Tweet(models.Model):
    body = models.TextField(max_length=240)
    timestamp = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
