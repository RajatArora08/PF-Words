from flask import Flask, request, render_template, jsonify
import SolrSearch

app = Flask(__name__)


@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)


@app.route('/send')
def send():
    query = request.args['query']
    option = request.args['options']

    data = SolrSearch.search(query, option)
    return render_template('result.html', data=data)


if __name__ == "__main__":
    app.run()
