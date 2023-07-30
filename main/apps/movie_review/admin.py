from django.contrib import admin
from main.apps.movie_review.models import MovieReview


@admin.register(MovieReview)
class MovieReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
