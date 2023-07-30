from typing import Any, Dict
from django.urls import reverse
from django.views import generic
from main.apps.movie_review.forms import MovieReviewForm
from main.apps.movie_review.models import MovieReview
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = "movie_review/index.html"
    context_object_name = "reviews"
    model = MovieReview
    paginate_by = 8

    def get_context_data(self, **kwargs):
        kwargs["form"] = MovieReviewForm()
        return super().get_context_data(**kwargs)


class MovieReviewCreateView(generic.CreateView):
    form_class = MovieReviewForm

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        context = self.get_context_data()
        context.update(csrf(self.request))
        form_html = render_crispy_form(form, context=context)
        return JsonResponse({"success": False, "form_html": form_html})

    def get_success_url(self):
        return reverse("moviereviews:index")


class SearchView(IndexView):
    template_name = "movie_review/partials/reviews.html"

    def get_queryset(self):
        title = self.request.GET.get("title", "")
        return MovieReview.objects.filter(title__icontains=title)
