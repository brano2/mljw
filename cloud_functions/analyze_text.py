from flask import jsonify
import pandas as pd
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def process_annotations(annotations):
    content = []
    sentiment = []
    magnitude = []

    for entity in annotations.entities:
        content.append(entity.name)
        sentiment.append(entity.sentiment.score)
        magnitude.append(entity.sentiment.magnitude)

    df = pd.DataFrame({"content": content, "sentiment": sentiment, "magnitude": magnitude})
    df = df.sort_values(['magnitude'], ascending=False)

    return df.to_json()


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
        return jsonify(result)
    else:
        return 'error'
