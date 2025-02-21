import pytest
import pickle
from unittest.mock import patch, MagicMock
from training_data_retriever.errors import TrainingDataRetrieverError
from training_data_retriever.wikipedia_article_name_retriever import WikipediaArticleNameRetriever


def mock_wikipedia_response():
    return {
        "items": [{
            "articles": [{"article": f"Article_{i}"} for i in range(100)]
        }]
    }


@pytest.fixture
def retriever():
    return WikipediaArticleNameRetriever()


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


@patch.object(WikipediaArticleNameRetriever, "_retrieve_articles_names", return_value=["Article_1", "Article_2"])
def test_get_data(mock_retrieve, retriever):
    retriever.get_data()
    assert retriever._article_names == ["Article_1", "Article_2"]


@patch("pickle.dump")
def test_save(mock_pickle_dump, retriever):
    retriever._article_names = ["Article_1"]
    with patch("builtins.open", MagicMock()):
        retriever.save()
    mock_pickle_dump.assert_called_once()

@patch("pickle.load", return_value=["Article_1"])
def test_load(mock_pickle_load, retriever):
    with patch("builtins.open", MagicMock()):
        result = retriever.load()
    assert result == ["Article_1"]

@patch("builtins.open", side_effect=FileNotFoundError)
@patch.object(WikipediaArticleNameRetriever, "get_data")
def test_load_not_found(mock_get_data, mock_pickle_load, retriever):
    retriever.load()
    mock_get_data.assert_called_once()