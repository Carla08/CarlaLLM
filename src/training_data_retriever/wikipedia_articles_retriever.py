import pickle
from datetime import datetime, timedelta

import requests

from training_data_retriever.errors import TrainingDataRetrieverError
from training_data_retriever.training_data_retriever_abc import TrainingDataRetriever


class WikipediaArticlesRetriever(TrainingDataRetriever):
    WIKIPEDIA_URL = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/"
    HEADERS = {"User-Agent": "MyWikipediaApp/1.0 (carlaprieto.com)"}

    def __init__(self):
        pass

    def get_data(self):
        return self._get_articles_links()

    def _create_article_link(self, article):
        return f"https://en.wikipedia.org/wiki/{article}"

    def _get_articles_links(self):
        try:
            file = open('articles_links.pkl', 'rb')
        except FileNotFoundError:
            article_links = self._retrieve_articles_names()
            with open('articles_links.pkl', 'wb') as out:
                pickle.dump(article_links, out, pickle.HIGHEST_PROTOCOL)
            return article_links
        else:
            article_links = pickle.load(file)
            return article_links

    def _retrieve_articles_names(self):
        yesterday = (datetime.utcnow() - timedelta(days=2)).strftime("%Y/%m/%d")
        url = f"{self.WIKIPEDIA_URL}{yesterday}"
        response = requests.get(url, headers=self.HEADERS)
        articles_names = []

        if response.status_code == 200:
            data = response.json()
            articles = data["items"][0]["articles"][:100]  # Get top 100 articles
            for article in articles:
                articles_names.append(self._create_article_link(article["article"]))
            return articles_names
        else:
            raise TrainingDataRetrieverError(
                f"Failed to fetch Wikipedia latest articles names. "
                f"Wikipedia API responded with status {response.status_code}")

    def serialize(self):
        pass

    def save(self):
        pass

    def load(self):
        pass
