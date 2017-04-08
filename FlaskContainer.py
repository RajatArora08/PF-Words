from flask import Flask, request, render_template, jsonify
import SolrSearch

app = Flask(__name__)


@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)


@app.route('/index/prosite')
def return_search():
    query = request.args['query']
    option = request.args['option']
    return jsonify(SolrSearch.search(query, option))

if __name__ == "__main__":
    app.run()
