from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    auther = models.CharField(max_length=20)
    image = models.ImageField(upload_to='media', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,  null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'post'


class Comment(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(null=True)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment'


class Profile(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    contact = models.IntegerField(null=True)
    dob = models.DateField(default=False, null=True)
    gender = models.CharField(max_length=10, null=True)
    pic = models.ImageField(upload_to='profile', default="/static/images/user.png")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'profile'