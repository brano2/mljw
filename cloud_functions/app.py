from flask import Flask, request

from hello_world import hello_world
from analyze_text import analyze_text

app = Flask(__name__)


@app.route('/', methods=['POST'])
def call():
    return hello_world(request)


@app.route('/analyze_text', methods=['POST'])
def call_analyze_test():
    return analyze_text(request)


if __name__ == '__main__':
    app.run()
