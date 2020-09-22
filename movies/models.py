from django.db import models
from users.models import User


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    year = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField()
    tmdb_id = models.IntegerField()
    image = models.CharField(max_length=255, blank=False, null=False)
    favorited_by = models.ManyToManyField(User, related_name="favorites", blank=True)

    def __str__(self):
        return f"{self.title}"