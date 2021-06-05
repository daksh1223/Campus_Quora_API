from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Community(models.Model):
    name = models.TextField(unique=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"id:{self.id} {self.name}"


class Question(models.Model):
    title = models.TextField()
    content = models.TextField()
    date = models.DateField(default=datetime.date.today)
    communities = models.ManyToManyField(Community)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('title', 'content',)

    def __str__(self):
        return f"id:{self.id} {self.title}"


class Answer(models.Model):
    content = models.TextField()
    date = models.DateField(default=datetime.date.today)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"id:{self.id} {self.content[:30]}"


class Comment(models.Model):
    content = models.TextField()
    date = models.DateField(default=datetime.date.today)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"id:{self.id} {self.content[:30]}"
