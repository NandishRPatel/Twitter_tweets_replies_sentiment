from django.db import models

# Create your models here.

class Tweets(models.Model):
    Lang = models.CharField(max_length=10)
    Day_time_date = models.CharField(max_length=30)
    Text = models.CharField(max_length=400)
    Fav_count = models.CharField(max_length=10)
    Ret_count = models.CharField(max_length=10)
    tweet_id = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    no_followers = models.CharField(max_length=10)
    toxic = models.CharField(max_length=10)
    urls = models.CharField(max_length=200)
    replies = models.CharField(max_length=200)
