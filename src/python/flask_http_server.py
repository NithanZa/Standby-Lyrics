from flask import Flask, request
from lyrics_fetcher import get_queue_lyrics

app = Flask(__name__)


@app.route('/hello')
def ping():
    return 'Hi!'


@app.route('/lyrics/<int:position>')
@app.route('/lyrics/<int:position>/updated')
def lyrics(position: int):
    return get_queue_lyrics(position, request.path.endswith("/new"))


if __name__ == '__main__':
    app.run(debug=True)
