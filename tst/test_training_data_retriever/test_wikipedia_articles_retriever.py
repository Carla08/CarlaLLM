import pytest
import requests
import requests_mock
from datetime import datetime, timedelta
from training_data_retriever.errors import TrainingDataRetrieverError
from training_data_retriever.wikipedia_articles_retriever import WikipediaArticlesRetriever


def test_wikipedia_articles_retriever_success():
    retriever = WikipediaArticlesRetriever()
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y/%m/%d")
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{yesterday}"

    mock_response = {
        "items": [{
            "articles": [
                {"article": "Python_(programming_language)"},
                {"article": "Machine_learning"},
                {"article": "Artificial_intelligence"}
            ]
        }]
    }

    with requests_mock.Mocker() as m:
        m.get(url, json=mock_response, status_code=200)
        articles = retriever.get()

    assert len(articles) == 3
    assert "Python_(programming_language)" in articles
    assert "Machine_learning" in articles
    assert "Artificial_intelligence" in articles


def test_wikipedia_articles_retriever_failure():
    retriever = WikipediaArticlesRetriever()
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y/%m/%d")
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{yesterday}"

    with requests_mock.Mocker() as m:
        m.get(url, status_code=500)
        with pytest.raises(TrainingDataRetrieverError, match="Failed to fetch Wikipedia Articles.*500"):
            retriever.get()


def test_wikipedia_articles_retriever_empty_response():
    retriever = WikipediaArticlesRetriever()
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y/%m/%d")
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{yesterday}"

    mock_response = {"items": [{"articles": []}]}  # No articles in the response

    with requests_mock.Mocker() as m:
        m.get(url, json=mock_response, status_code=200)
        articles = retriever.get()

    assert articles == []
