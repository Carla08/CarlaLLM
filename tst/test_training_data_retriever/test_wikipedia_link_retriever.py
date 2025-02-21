import pytest
import pickle
from unittest.mock import patch, MagicMock
from training_data_retriever.errors import TrainingDataRetrieverError
from training_data_retriever.wikipedia_link_retriever import WikipediaLinkRetriever


def mock_wikipedia_response():
    return {
        "items": [{
            "articles": [{"article": f"Article_{i}"} for i in range(100)]
        }]
    }


@pytest.fixture
def retriever():
    return WikipediaLinkRetriever()


@patch("requests.get")
def test_retrieve_articles_names(mock_get, retriever):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_wikipedia_response()

    article_names = retriever._retrieve_articles_names()
    assert len(article_names) == 100
    assert article_names[0] == "Article_0"


@patch("requests.get")
def test_retrieve_articles_names_failure(mock_get, retriever):
    mock_get.return_value.status_code = 500

    with pytest.raises(TrainingDataRetrieverError):
        retriever._retrieve_articles_names()


@pytest.mark.parametrize("article, expected_link", [
    ("Python_(programming_language)", "https://en.wikipedia.org/wiki/Python_(programming_language)"),
    ("Machine_learning", "https://en.wikipedia.org/wiki/Machine_learning")
])
def test_create_article_link(retriever, article, expected_link):
    assert retriever._create_article_link(article) == expected_link


@patch.object(WikipediaLinkRetriever, "_retrieve_articles_names", return_value=["Article_1", "Article_2"])
def test_get_data(mock_retrieve, retriever):
    retriever.get_data()
    assert retriever._article_names == ["Article_1", "Article_2"]
    assert retriever._article_links == [
        "https://en.wikipedia.org/wiki/Article_1",
        "https://en.wikipedia.org/wiki/Article_2"
    ]


@patch("pickle.dump")
def test_save(mock_pickle_dump, retriever):
    retriever._article_links = ["https://en.wikipedia.org/wiki/Article_1"]
    with patch("builtins.open", MagicMock()):
        retriever.save()
    mock_pickle_dump.assert_called_once()

@patch("pickle.load", return_value=["https://en.wikipedia.org/wiki/Article_1"])
def test_load(mock_pickle_load, retriever):
    with patch("builtins.open", MagicMock()):
        result = retriever.load()
    assert result == ["https://en.wikipedia.org/wiki/Article_1"]

@patch("builtins.open", side_effect=FileNotFoundError)
@patch.object(WikipediaLinkRetriever, "get_data")
def test_load_not_found(mock_get_data, mock_pickle_load, retriever):
    retriever.load()
    mock_get_data.assert_called_once()