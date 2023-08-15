from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from main.apps.movie_review.forms import MovieReviewForm
from main.apps.movie_review.models import MovieReview
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.http import HttpResponse, JsonResponse


class IndexView(ListView):
    template_name = "movie_review/index.html"
    context_object_name = "reviews"
    model = MovieReview
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs["form"] = MovieReviewForm()
        return super().get_context_data(**kwargs)


class SearchView(IndexView):
    template_name = "movie_review/partials/list.html"

    def get_queryset(self):
        title = self.request.GET.get("title", "")
        return MovieReview.objects.filter(title__icontains=title)


class MovieReviewCreateView(CreateView):
    form_class = MovieReviewForm

    def form_valid(self, form):
        super().form_valid(form)

        context = self.get_context_data()
        context.update(csrf(self.request))
        form = MovieReviewForm()
        form_html = render_crispy_form(form, context=context)

        response = HttpResponse(form_html)
        response["HX-Trigger"] = "closeModal"
        return response

    def form_invalid(self, form):
        context = self.get_context_data()
        context.update(csrf(self.request))
        form_html = render_crispy_form(form, context=context)

        response = HttpResponse(form_html)
        return response

    def get_success_url(self):
        return reverse("moviereviews:index")


class MovieReviewUpdateView(MovieReviewCreateView, UpdateView):
    form_class = MovieReviewForm
    model = MovieReview

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data()
        context.update(csrf(request))
        form_html = render_crispy_form(context["form"], context=context)

        response = HttpResponse(form_html)
        return response

    def form_valid(self, form):
        super().form_valid(form)

        response = HttpResponse()
        response["HX-Trigger"] = "closeModal"
        response["HX-Reswap"] = "none"
        return response
