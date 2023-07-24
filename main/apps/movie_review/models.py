from django.db import models


class MovieReview(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.CharField(max_length=200)
    image_height = models.IntegerField()
    image_width = models.IntegerField()
