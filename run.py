# -*- coding: utf-8 -*-
from backend.models.template import Template
from backend.models.page import Article
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
CORS(app)

template = ""
Article.read_tfidf()

@app.route('/api/template', methods=['GET'])
def get_template():
    # URLパラメータ
    params = request.args
    response = {}
    keys = []
    global template

    if 'keywords' in params:
        keys = params.get('keywords').split(":")
        print(keys)
    template = Template({"keys":keys})
    if template.select_similar():
        template.recommended_infobox()
        template.recommended_sections()

        response['result'] = 'Success'
        response['infobox'] = template.infobox.to_dict()
        response['sections'] = template.secs
        response['wiki'] = template.to_wiki()
    else:
        response['result'] = 'Not found articles matching to keywords'
    return make_response(jsonify(response))

@app.route('/api/similars', methods=['GET'])
def get_similars():
    global template
    response = {}
    response['similars'] = [{'title': s.title, 'infobox': template.ib_title(s.infobox), 'sections': s.secs} for s in template.similars]
    return make_response(jsonify(response))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
