import os

from flask import jsonify
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import numpy as np
import pandas as pd
import webhoseio

WEBHOSE_TOK = os.getenv('WEBHOSEIO_TOKEN')
if WEBHOSE_TOK is None:
    print('ERROR: WEBHOSEIO_TOKEN environment variable not set!')
webhoseio.config(token=WEBHOSE_TOK)


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


def select_article(similar_articles, original_art_stats):
    keywords = original_art_stats.content[:5]
    orig_sentiments = original_art_stats.sentiment[:5]
    corr_coefs = []
    art_stats = []
    for art in similar_articles:
        text = art.get('text')
        df = process_annotations(get_annotations(text))
        sentiments = []
        for kw in keywords:
            sentiment = df.loc[df.content == kw].sentiment.values
            if sentiment.size > 0:
                sentiments.append(sentiment[0])  # There will be at most one sentiment
            else:
                sentiments.append(0)
        corr_coefs.append(np.corrcoef(orig_sentiments, sentiments)[0, 1])
        art_stats.append((df, sentiments, corr_coefs[-1]))
    i = np.argmin(corr_coefs)
    return similar_articles[i], art_stats


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
        recommendation, art_stats = select_article(similar_articles, result)

        
        # print(len(recommendations_prep))
        # for each similar articles get result from Google NLP API and recommend article (use get_annotations on similar_articles[N].content)
        return jsonify([recommendation])
    else:
        return 'error'