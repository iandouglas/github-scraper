from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/<string:site>/<string:account>/<string:repo>')
def scraper_nometadata(site, account, repo):
    return scraper(site, account, repo, None)


@app.route('/<string:site>/<string:account>/<string:repo>/<string:metadata>')
def scraper(site, account, repo, metadata):
    url = 'https://{site}/{account}/{repo}'.format(
        site=site,
        account=account,
        repo=repo,
    )
    counters = []

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    counters = soup.select(".Counter")
    counter_position = None

    if metadata:
        if metadata == 'issues':
            counter_position = 0
        elif metadata == 'pull_requests':
            counter_position = 1
        return jsonify(counters[counter_position].contents[0])


    return jsonify({
        'issues': counters[0].contents[0],
        'pull_requests': counters[1].contents[0],
    })

if __name__ == '__main__':
    app.run(debug=True)
