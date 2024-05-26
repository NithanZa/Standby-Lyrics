from flask import Flask, request
from lyrics_fetcher import get_queue_lyrics

app = Flask(__name__)


@app.route('/hello')
def ping():
    return 'Hi!'


@app.route('/lyrics/<int:position>')
@app.route('/lyrics/<int:position>/updated')
def lyrics(position: int):
    return get_queue_lyrics(position, not request.path.endswith("/updated"))


def run_app():
    app.run(debug=True)
