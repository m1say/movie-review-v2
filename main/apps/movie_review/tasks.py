import logging
from main.celery import app
from django.conf import settings
from main.utils.api_client import NYTimesAPIClient
from main.apps.movie_review.models import MovieReview

logger = logging.getLogger(__name__)

@app.task(bind=True)
def sync_movie_reviews(self):
    api_client = NYTimesAPIClient(
        host=settings.NY_TIMES_HOST,
        api_key=settings.NY_TIMES_API_KEY
    )

    results = api_client.get_movie_reviews()
    for result in results:
        MovieReview.objects.update_or_create(
            title=result["display_title"],
            headline=result["headline"],
            summary=result["summary_short"],
            publication_date=result["publication_date"],
            link=result["link"]["url"],
            image_url=result["multimedia"]["src"],
            image_height=result["multimedia"]["height"],
            image_width=result["multimedia"]["width"],
        )
