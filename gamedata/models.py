from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Game_type(models.Model):
    type_name = models.CharField(max_length=50)

class Game(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(max_length=255, blank=True, null=True)
    game_type_id = models.ForeignKey(Game_type, on_delete=models.CASCADE)
    developer = models.CharField(max_length=50)
    rating = models.CharField(max_length=5, null=True)
    release_date = models.DateField(null=True)
    price = models.FloatField()

class User_games(models.Model): 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    purchased_date = models.DateField(auto_now_add=True)
    serial = models.CharField(max_length=255, unique=True)

class Image(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    Image_url = models.ImageField(upload_to='static/static_dirs/images/')


