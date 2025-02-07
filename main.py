from dependency.dependency_manager import DependencyManager
import dependency.dependencies as d


dm = DependencyManager()
training_data_retriever = dm.get(d.TRAINING_DATA_RETRIEVER)
wiki_articles = training_data_retriever.get()

for i, article in enumerate(wiki_articles, start=1):
    print(f"{i}. {article}")