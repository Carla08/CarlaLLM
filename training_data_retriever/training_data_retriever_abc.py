from abc import ABC, abstractmethod


class TrainingDataRetriever(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass
