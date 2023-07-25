from django.db import models


class MovieReview(models.Model):
    title = models.CharField(max_length=200)
    headline = models.TextField()
    summary = models.TextField()
    publication_date = models.DateField()
    link = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    image_height = models.IntegerField()
    image_width = models.IntegerField()

    def __str__(self):
        return self.title