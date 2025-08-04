from django.db import models
from django.contrib.auth.models import User #Imports Django built-in User model

# Create your models here.

class Topic(models.Model):
    # Represents a topic in the dictionary, which is like headline.
    title = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Entry(models.Model):

    # Represents an entry(comment) under a specific topic.

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1024, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Entry for "{self.topic.title}" by {self.author.username}'