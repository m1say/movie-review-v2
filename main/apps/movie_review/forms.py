from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Layout, Reset, Submit
from django.forms import ModelForm, Textarea, ValidationError
from django.urls import reverse
from validators.url import url

from main.apps.movie_review.models import MovieReview


class MovieReviewForm(ModelForm):
    class Meta:
        model = MovieReview
        fields = ["title", "headline", "summary", "link", "image"]
        widgets = {
            "headline": Textarea(attrs={"rows": 2}),
            "summary": Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = True

        self.fields["image"].required = False

        url = reverse("moviereviews:create")
        if self.instance and self.instance.pk:
            url = reverse("moviereviews:update", kwargs={"pk": self.instance.pk})

        self.helper = FormHelper()
        self.helper.form_id = "review-form"
        self.helper.attrs = {
            "hx-post": url,
            "hx-target": "this",
            "hx-swap": "outerHTML",
        }

        self.helper.layout = Layout(
            Div(
                "title", "headline", "summary", "link", "image", css_class="modal-body"
            ),
            Div(
                Reset("reset", "Reset", hidden=True),
                Button(
                    "cancel",
                    "Cancel",
                    css_class="btn-secondary",
                    data_bs_dismiss="modal",
                ),
                Submit("submit", "Submit", css_class="button white"),
                css_class="modal-footer",
            ),
        )

    def clean_link(self):
        link = self.cleaned_data["link"]
        if not url(link):
            raise ValidationError("Please provide a valid link")
        return link
