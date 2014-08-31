__author__ = 'mnewman'

from birdy.twitter import AppClient
from flask import Flask, jsonify, request

CONSUMER_KEY = 'z17kVPGuf7bp7iVn2gcvTtlPc'
CONSUMER_SECRET = 'E7Oq55hJYUI1SlJgFNhvtnrl3KfXfTSkyfNGgV6z7mTIbkDfcq'


class TestAppClient(AppClient):
    @staticmethod
    def get_json_object_hook(data):
        return data


client = TestAppClient(CONSUMER_KEY, CONSUMER_SECRET)
access_token = client.get_access_token()
client = TestAppClient(CONSUMER_KEY, CONSUMER_SECRET, access_token)


def get_tweets(topic, count):
    return client.api.search.tweets.get(q=topic, count=count).data.get('statuses')


def get_embed_html(id):
    return client.api.statuses.oembed.get(id=id).data.get('html')

##########

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route("/tweets")
def tweets():
    topic = request.args.get('q')
    count = request.args.get('count')
    return jsonify({'tweets': get_tweets(topic, count)})

@app.route("/embedData")
def embed_data():
    id = request.args.get('id')
    return jsonify({'html': get_embed_html(id)})

##########

if __name__ == "__main__":
    app.run(debug=True)

##########

