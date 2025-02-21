import pickle
from datetime import datetime, timedelta

import requests

from training_data_retriever.errors import TrainingDataRetrieverError
from training_data_retriever.training_data_retriever_abc import TrainingDataRetriever


class WikipediaArticlesRetriever(TrainingDataRetriever):

    def __init__(self):
        pass

    def get_data(self):
        pass

    def serialize(self):
        pass

    def save(self):
        pass

    def load(self):
        pass
