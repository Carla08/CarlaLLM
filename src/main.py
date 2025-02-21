from training_data_retriever.wikipedia_articles_retriever import WikipediaArticlesRetriever
from training_data_retriever.wikipedia_link_retriever import WikipediaLinkRetriever


training_data_retriever = WikipediaLinkRetriever()
wiki_articles = training_data_retriever.get_data()

for i, article in enumerate(wiki_articles, start=1):
    print(f"{i}. {article}")