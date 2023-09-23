from django.urls import path

from . import views

app_name = "moviereviews"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("search", views.SearchView.as_view(), name="search"),
    path("create", views.MovieReviewCreateView.as_view(), name="create"),
    path("update/<int:pk>", views.MovieReviewUpdateView.as_view(), name="update"),
]
