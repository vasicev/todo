from django.db import models

class Tag(models.Model):

    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Task(models.Model):

    tag = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
