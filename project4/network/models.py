from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    # need symmetrical false to make many to many relationship unidirectional
    following = models.ManyToManyField('self', blank=True, symmetrical=False)
    followers = models.IntegerField(default=0)
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    time = models.DateTimeField(default=now)
    # need a related name that is diffrent from other names when you reference a table
    # twice. In this case I reference the User table in the user field and in the like field
    # so I added a related name to like field. You wont actually have to use the related name though.
    like = models.ManyToManyField(
        User, blank=True, symmetrical=False, related_name="user_like")
