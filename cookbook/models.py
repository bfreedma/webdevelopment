from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db.models import Avg
# Create your models here.

class User(AbstractUser):
    recipes = models.ManyToManyField('Recipe', blank=True, symmetrical=False)
    following = models.ManyToManyField('self', blank=True, symmetrical=False)
    followers = models.IntegerField(default=0)
    pass


#models auto include a unique id.
class Recipe(models.Model):
    name = models.CharField(max_length=150, blank = False)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank = False)
    directions = models.TextField(blank = False)
    image = models.ImageField(upload_to='images/')
    time = models.DateTimeField(default=now)
    reviews = models.ManyToManyField('Review', blank=True, symmetrical=False)
    def avg_ratings(self):
        return self.reviews.aggregate(Avg('rating'))
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    time = models.DateTimeField(default=now)
    rating = models.IntegerField()
    like = models.ManyToManyField(
        User, blank=True, symmetrical=False, related_name="user_like")
