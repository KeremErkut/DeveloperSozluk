from django.db import models

# Create your models here.
class User(models.Model):

    # 1-)Custom user setup for simplicity and MVP goals. In real-world situations,
    # it's often better to extend Django's built-in User model.

    # 2) If you're wondering why we didn't define a unique user_id, the answer is that
    # Django automatically creates a unique identifier for every object in the table, regardless
    # of whether we define an ID field or not.


    username = models.CharField(max_length=50, unique=False,null=False, blank=False)

    # LLM generated 'username' like that:
    # username = models.CharField(max_length=50, unique=True)
    # I am not looking for uniqueness. That's why I 'll stand with this definition.

    def __str__(self):
        return self.username

class Topic(models.Model):

    # Represents a topic in the dictionary, which is like headline.


    title = models.CharField(max_length=100, unique=True, null=False, blank=False,
                             help_text="This area can not be empty and must be unique.")
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