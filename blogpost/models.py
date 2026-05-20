from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import User
# Create your models here.

class CustomUser(AbstractUser, PermissionsMixin):
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)


class OneTimePassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=10, unique=True)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Comments(models.Model):
    commenter = models.CharField(max_length=200)
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.comment