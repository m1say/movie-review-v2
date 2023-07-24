from django.shortcuts import render
from django.views import generic, View
from main.apps.movie_review.models import MovieReview

class IndexView(View):
    template_name = 'movie_review/index.html'

    def queryset(self):
        return MovieReview.objects.all()

    def get(self, request, *args, **kwargs):
        context = {
            "queryset": self.queryset()
        }
        return render(request, self.template_name, context)
