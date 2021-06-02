from django.db import models
from django.contrib.auth.models import User
import datetime 
# Create your models here.

class Community(models.Model):
    name = models.TextField(unique=True)
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.TextField()
    content = models.TextField()
    date = models.DateField(default=datetime.date.today)
    communities = models.ManyToManyField(Community)
    user = models.ForeignKey(User,models.CASCADE)
    class Meta:
        unique_together = ('title','content',)
    def __str__(self):
        return f"{self.id} {self.title}"
