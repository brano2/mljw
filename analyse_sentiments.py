import argparse
import os

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account

# def print_results(annotations):



#   print(annotations)

def analyze(movie_review_filename):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    with open(movie_review_filename, 'r') as review_file:
        # Instantiates a plain text document.
        content = review_file.read()

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_entity_sentiment(document=document)

    # Print the results
    print_results(annotations)


if __name__ == '__main__':
    
    analyze("article.txt")