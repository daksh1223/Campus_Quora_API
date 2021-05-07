from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class category(models.Model):
    category=models.CharField(max_length=100,default="none")
    def __str__(self):
        return self.category