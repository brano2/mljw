from flask import jsonify
import pandas as pd
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def print_results(annotations):
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

def analyze(text):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_entity_sentiment(document=document)

    # Print the results
    text = print_results(annotations)
    return text
    
def hello_world(request):
    request_json = request.get_json()
    if request_json and 'text' in request_json:
        res = analyze(request_json['text'])
        return jsonify(res)
    else:
        return 'error'