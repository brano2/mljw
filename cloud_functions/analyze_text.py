import os

from flask import jsonify
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from newsapi import NewsApiClient
import pandas as pd


def process_annotations(annotations):
    content = []
    salience = []
    sentiment = []
    magnitude = []

    for entity in annotations.entities:
        content.append(entity.name)
        salience.append(entity.salience)
        sentiment.append(entity.sentiment.score)
        magnitude.append(entity.sentiment.magnitude)

    df = pd.DataFrame({"content": content, "salience": salience, "sentiment": sentiment, "magnitude": magnitude})
    df = df.iloc[0:20].sort_values(['magnitude'], ascending=False)

    return df

def _build_query(phrases):
    return ' '.join([f'"{phrase}"' if ' ' in phrase else phrase for phrase in phrases])

def find_related_articles(df):
    newsapi = NewsApiClient(api_key=os.getenv('NEWSAPI_KEY'))
    n_keywords = 5
    articles = []
    while len(articles) < 10:
        query = _build_query(df.content[:n_keywords])
        search_results = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        articles.extend(search_results['articles'])
        n_keywords -= 1

    return articles


def get_annotations(text):
    """Run a sentiment analysis request on text."""
    client = language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_entity_sentiment(document=document)

    return annotations


def analyze_text(request):
    request_json = request.get_json()
    if request_json and 'text' in request_json:
        annotations = get_annotations(request_json['text'])
        result = process_annotations(annotations)
        similar_articles = find_related_articles(result)
        # for each similar articles get result from Google NLP API and recommend article (use get_annotations on similar_articles[N].content)

        return jsonify(result.to_json())
    else:
        return 'error'
