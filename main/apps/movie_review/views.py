from django.shortcuts import render
from django.views import generic, View

class IndexView(View):
    template_name = 'movie_review/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
