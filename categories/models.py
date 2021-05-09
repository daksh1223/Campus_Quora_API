from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Comment(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     comment=models.TextField()
     def __str__(self):
         return self.comment[0:50]


class Post(models.Model):
    post = models.TextField()
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    like = models.ManyToManyField(User, related_name="likes",blank=True)
    comment=models.ManyToManyField(Comment,blank=True)
    def __str__(self):
        return self.post[0:50]

class Question(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ManyToManyField(Post, blank=True)
    question = models.CharField(max_length=100, default="None")

    def __str__(self):
        return self.question[0:50]

class Category(models.Model):
    category = models.CharField(max_length=100, default="None")
    questions = models.ManyToManyField(Question,blank=True)

    def __str__(self):
        return self.category



