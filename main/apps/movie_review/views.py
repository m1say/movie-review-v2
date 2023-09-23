from crispy_forms.utils import render_crispy_form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from main.apps.movie_review.forms import MovieReviewForm
from main.apps.movie_review.models import MovieReview


class CustomPaginator(Paginator):
    def validate_number(self, number):
        if isinstance(number, str) and number == "last":
            number = self.num_pages
        return super().validate_number(number)


class IndexView(ListView):
    template_name = "movie_review/index.html"
    context_object_name = "reviews"
    model = MovieReview
    paginate_by = 9
    paginator_class = CustomPaginator

    def get_context_data(self, **kwargs):
        kwargs["form"] = MovieReviewForm()
        return super().get_context_data(**kwargs)


class SearchView(IndexView):
    template_name = "movie_review/partials/list.html"

    def get_queryset(self):
        title = self.request.GET.get("title", "")
        return MovieReview.objects.filter(title__icontains=title)


class MovieReviewCreateView(LoginRequiredMixin, CreateView):
    form_class = MovieReviewForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()

        context = self.get_context_data()
        context.update(csrf(self.request))

        form = MovieReviewForm()
        form_html = render_crispy_form(form, context=context)
        toast_html = render_to_string(
            template_name="movie_review/partials/toast.html",
            context={
                "action": "Success!",
                "message": f"Successfully created {self.object.title}.",
            },
            request=self.request,
        )

        content = toast_html + form_html
        response = HttpResponse(content)
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
        self.object = form.save()

        response = render(
            self.request,
            "movie_review/partials/toast.html",
            context={
                "action": "Success!",
                "message": f"Successfully updated {self.object.title}.",
            },
        )
        response["HX-Trigger"] = "closeModal"
        response["HX-Reswap"] = "beforeend"
        response["HX-Retarget"] = "#toasts"
        return response
