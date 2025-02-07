from datetime import datetime, timedelta

import requests

from training_data_retriever.training_data_retriever_abc import TrainingDataRetriever
from training_data_retriever.errors import TrainingDataRetrieverError


class WikipediaArticlesRetriever(TrainingDataRetriever):
    WIKIPEDIA_URL = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/"
    HEADERS = {"User-Agent": "MyWikipediaApp/1.0 (carlaprieto.com)"}

    def __init__(self):
        pass

    def get(self):
        yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y/%m/%d")
        url = f"{self.WIKIPEDIA_URL}{yesterday}"
        response = requests.get(url, headers=self.HEADERS)

        if response.status_code == 200:
            data = response.json()
            articles = data["items"][0]["articles"][:100]  # Get top 100 articles
            return [article["article"] for article in articles]
        else:
            raise TrainingDataRetrieverError(
                f"Failed to fetch Wikipedia Articles. Wikipedia API responded with status {response.status_code}")

    def serialize(self):
        pass

    def save(self):
        pass

    def load(self):
        pass
