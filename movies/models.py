from django.db import models
from users.models import User


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    release_date = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField()
    tmdb_id = models.IntegerField()
    imageURL = models.CharField(max_length=255, blank=False, null=False)
    favorited_by = models.ManyToManyField(User, related_name="favorites", blank=True)