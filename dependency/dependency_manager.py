import dependency.dependencies as d
from training_data_retriever.wikipedia_articles_retriever import WikipediaArticlesRetriever


class DependencyManager:
    DEPENDENCIES_MAP = {}

    def __init__(self):
        pass

    def get(self, s):
        if s in self.DEPENDENCIES_MAP:
            return self.DEPENDENCIES_MAP[s]
        else:
            if s in self.LOADER_DEPENDENCIES_MAP:
                self.DEPENDENCIES_MAP[s] = self.LOADER_DEPENDENCIES_MAP[s](self)
                return self.DEPENDENCIES_MAP[s]
            else:
                raise KeyError(f"Dependency {s} initializer not found.")

    def _load_training_data_retriever(self):
        return WikipediaArticlesRetriever()

    LOADER_DEPENDENCIES_MAP = {
        d.TRAINING_DATA_RETRIEVER: _load_training_data_retriever
    }
