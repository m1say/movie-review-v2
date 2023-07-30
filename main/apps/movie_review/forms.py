from django.forms import ModelForm, Textarea, ValidationError
from django.utils import timezone
from validators.url import url
from main.apps.movie_review.models import MovieReview
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button


class MovieReviewForm(ModelForm):
    class Meta:
        model = MovieReview
        fields = [
            "title",
            "headline",
            "summary",
            "link",
            "image_url",
        ]
        widgets = {
            "headline": Textarea(attrs={"rows": 2}),
            "summary": Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = True

        self.helper = FormHelper()
        self.helper.form_id = "review-form"
        self.helper.form_method = "post"

    def clean_link(self):
        link = self.cleaned_data["link"]
        if not url(link):
            raise ValidationError("Please provide a valid link")
        return link

    def clean_image_url(self):
        image_url = self.cleaned_data["image_url"]
        if not url(image_url):
            raise ValidationError("Please provide a valid image url")
        return image_url
