import pytest
import requests
import requests_mock
import pickle
from datetime import datetime, timedelta
from training_data_retriever.errors import TrainingDataRetrieverError
from training_data_retriever.wikipedia_articles_retriever import WikipediaArticlesRetriever


def test_wikipedia_articles_retriever_success(mocker):
    retriever = WikipediaArticlesRetriever()
    yesterday = (datetime.utcnow() - timedelta(days=2)).strftime("%Y/%m/%d")
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

    cached_articles = [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://en.wikipedia.org/wiki/Machine_learning",
        "https://en.wikipedia.org/wiki/Artificial_intelligence"
    ]
    with requests_mock.Mocker() as m:
        m.get(url, json=mock_response, status_code=200)
        mock_open = mocker.mock_open()
        mocker.patch("builtins.open", mock_open)
        mock_pickle_dump = mocker.patch("pickle.dump")
        mock_pickle_load = mocker.patch("pickle.load", return_value=cached_articles)

        articles = retriever.get_data()

    assert len(articles) == 3
    assert "https://en.wikipedia.org/wiki/Python_(programming_language)" in articles
    assert "https://en.wikipedia.org/wiki/Machine_learning" in articles
    assert "https://en.wikipedia.org/wiki/Artificial_intelligence" in articles


def test_wikipedia_articles_retriever_failure(mocker, requests_mock):
    retriever = WikipediaArticlesRetriever()
    yesterday = (datetime.utcnow() - timedelta(days=2)).strftime("%Y/%m/%d")
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{yesterday}"

    # Mock the 'open' function to raise a FileNotFoundError
    mocker.patch("builtins.open", side_effect=FileNotFoundError)

    # Using the requests_mock fixture to mock the request globally
    requests_mock.get(url, status_code=500)

    with pytest.raises(TrainingDataRetrieverError):
        retriever.get_data()



def test_wikipedia_articles_retriever_cache(mocker):
    retriever = WikipediaArticlesRetriever()
    cached_articles = [
        "https://en.wikipedia.org/wiki/Deep_learning",
        "https://en.wikipedia.org/wiki/Data_science"
    ]
    binary_data = pickle.dumps(cached_articles)  # Ensure the data is binary
    mock_open = mocker.mock_open(read_data=binary_data)  # Simulate reading from a binary file

    mocker.patch("builtins.open", mock_open)
    mocker.patch("pickle.load", return_value=cached_articles)

    articles = retriever.get_data()
    assert articles == cached_articles
