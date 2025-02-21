import pickle
from datetime import datetime, timedelta

import requests

from training_data_retriever.errors import TrainingDataRetrieverError
from training_data_retriever.training_data_retriever_abc import TrainingDataRetriever


class WikipediaArticleNameRetriever(TrainingDataRetriever):
    WIKIPEDIA_URL = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/"
    HEADERS = {"User-Agent": "MyWikipediaApp/1.0 (carlaprieto.com)"}

    def __init__(self):
        super().__init__()
        self._article_names = None

    def get_data(self):
        self._article_names = self._retrieve_articles_names()
        self.save()
        return self._article_names

    def _retrieve_articles_names(self):
        yesterday = (datetime.utcnow() - timedelta(days=2)).strftime("%Y/%m/%d")
        url = f"{self.WIKIPEDIA_URL}{yesterday}"
        response = requests.get(url, headers=self.HEADERS)

        if response.status_code == 200:
            data = response.json()
            articles = data["items"][0]["articles"][:100]  # Get top 100 articles
            return [article['article'] for article in articles]
        else:
            raise TrainingDataRetrieverError(
                f"Failed to fetch Wikipedia latest articles names. "
                f"Wikipedia API responded with status {response.status_code}")

    def serialize(self):
        return self._article_names

    def save(self):
        with open('articles_links.pkl', 'wb') as out:
            pickle.dump(self._article_names, out, pickle.HIGHEST_PROTOCOL)

    def load(self):
        try:
            file = open('articles_links.pkl', 'rb')
        except FileNotFoundError:
            self.get_data()
        else:
            self._article_names = pickle.load(file)
            return self._article_names
