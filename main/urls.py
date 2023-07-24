from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.apps.movie_review.urls')),
    path('admin/', admin.site.urls),
]
