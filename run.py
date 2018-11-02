# -*- coding: utf-8 -*-
from backend.models.template import Template
from backend.models.page import Article
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

@app.route("/api/template", methods=['GET'])
def get_template():
    # URLパラメータ
    params = request.args
    response = {}
    keys = []
    title = ""

    if 'keywords' in params:
        keys = params.get('keywords').split(":")
    if 'title' in params:
        title = params.get('title')
    template = Template({"title":title, "keys":keys})
    if template.select_similar():
        template.recommended_infobox()
        template.recommended_sections()

    response["wiki"] = template.to_wiki()
    return make_response(jsonify(response))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    Article.read_tfidf()
    app.run()
