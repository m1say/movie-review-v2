import logging
from time import sleep
from django.conf import settings
import requests
import re
from requests import HTTPError
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import requests_mock
from requests_mock.response import create_response


logger = logging.getLogger(__name__)


def raise_and_log_error(response, *args, **kwargs):
    try:
        response.raise_for_status()
    except HTTPError:
        logger.exception(
            "Got response with status code {}: {}".format(
                response.status_code, response.text
            )
        )
        raise
    return response


class MovieReviewMocker:
    service_path = "/svc/movies/v2/reviews/search.json"

    def get_response(self, request):
        json_data = {
            "status": "OK",
            "copyright": "Copyright (c) 2023 The New York Times Company. All Rights Reserved.",
            "has_more": False,
            "num_results": 1,
            "results": [
                {
                    "display_title": "The Venture Bros.: Radiant Is the Blood of the Baboon Heart",
                    "mpaa_rating": "R",
                    "critics_pick": 1,
                    "byline": "Danielle Dowling",
                    "headline": "‘The Venture Bros.: Radiant Is the Blood of the Baboon Heart’ Review: Return of the Glorious Weirdos",
                    "summary_short": "A beloved Adult Swim cartoon comes back to tie up some loose ends.",
                    "publication_date": "2023-07-20",
                    "opening_date": "2023-07-21",
                    "date_updated": "2023-07-20 21:04:34",
                    "link": {
                        "type": "article",
                        "url": "https://www.nytimes.com/2023/07/20/movies/the-venture-bros-radiant-is-the-blood-of-the-baboon-heart-review.html",
                        "suggested_link_text": "Read the New York Times Review of The Venture Bros.: Radiant Is the Blood of the Baboon Heart",
                    },
                    "multimedia": {
                        "type": "mediumThreeByTwo210",
                        "src": "https://static01.nyt.com/images/2023/07/20/multimedia/20venture-bros-art-2-ghvc/20venture-bros-art-2-ghvc-mediumThreeByTwo440.jpg",
                        "height": 140,
                        "width": 210,
                    },
                }
            ],
        }

        return create_response(request, json=json_data, status_code=200)


class NYTimesMatcher:
    def __init__(self):
        self.mockers = {}
        for m in (MovieReviewMocker(),):
            self.mockers[m.service_path] = m

    def __call__(self, request):
        request_pattern = request.path
        for request_path, mock in self.mockers.items():
            if re.match(request_pattern, request_path):
                return self.mockers[request_pattern].get_response(request)
        raise Exception(f"Unknown mock request received: {request_pattern}")


class NYTimesAPIClient:
    def __init__(self, host="", api_key=""):
        self.host = host
        self.api_key = api_key
        self.use_mocks = self.host.startswith("mock")

        session = requests.Session()
        session.hooks["response"] = [raise_and_log_error]

        if self.use_mocks:
            mock_adapter = requests_mock.Adapter()
            session.mount("mock", mock_adapter)
            mock_adapter.add_matcher(NYTimesMatcher())
        else:
            retry_strategy = Retry(
                total=3,
                status_forcelist=[429, 500, 503],
                allowed_methods=["GET"],
                backoff_factor=2,
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount(self.host, adapter)
        self.session = session

    def get_movie_reviews(self, offset=0, query="", **kwargs):
        url = f"{self.host}/svc/movies/v2/reviews/search.json"
        params = {"query": query, "api-key": self.api_key}

        reviews = []
        limit = settings.NY_TIMES_DATA_LIMIT

        while True:
            params["offset"] = offset
            response = self.session.request("GET", url=url, params=params)

            data = response.json()
            reviews.extend(data["results"] or [])
            if not data["has_more"]:
                break

            offset += data["num_results"]

            print(f"{offset=}")
            if limit and offset >= limit:
                break

            sleep(5)  # avoid 429

        return reviews


if __name__ == "__main__":
    settings.NY_TIMES_DATA_LIMIT = 5
    host = "mock://api.nytimes.com"
    api_key = ""
    api_client = NYTimesAPIClient(host=host, api_key=api_key)
    movie_reviews = api_client.get_movie_reviews()
