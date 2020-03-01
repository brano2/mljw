import os

from flask import jsonify
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from newsapi import NewsApiClient
import pandas as pd
import webhoseio
webhoseio.config(token="7399617f-00ac-48ec-9e6a-deb0d8912c65")


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
        query = _build_query(df.content[:n_keywords]) + " language:english"
        query_params = {
            "q": query,
            "ts": "1580463415153",
            "sort": "relevancy"
        }
        search_results = webhoseio.query("filterWebContent", query_params)
        # search_results = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        print(len(search_results['posts']))
        for article in search_results['posts']:
            if len(articles) < 10:
                articles.append(article)

        n_keywords -= 1

    return articles


def get_annotations(text):
    # print(type(text))
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

        recommendations_prep = []
        for art in similar_articles:
            text = art.get('text')
            # print(text)
            if text:
                temp_result = get_annotations(text)
                recommendations_prep.append(process_annotations(temp_result))

        
        # print(len(recommendations_prep))
        # for each similar articles get result from Google NLP API and recommend article (use get_annotations on similar_articles[N].content)

        return jsonify(result.to_json())
    else:
        return 'error'
