# -*- coding: utf-8 -*-
from backend.models.template import Template
from backend.models.page import Article
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from itertools import combinations

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
CORS(app)

template = ""
pairs = []
treat = 0
similars_len = 0

@app.route('/api/pairs', methods=['GET'])
def get_pairs():
    # URLパラメータ
    params = request.args
    response = {}
    keys = []
    global pairs
    global treat
    global similars_len
    pairs = []
    treat = 0
    similars_len = 0


    if 'keywords' in params:
        keys = params.get('keywords').split(":")
        print(keys)
        for key_num in reversed(range(len(keys) + 1)[1:]):
            print("キーワード数 {} の組合せ".format(key_num))
            for c in combinations(keys, key_num):
                pairs.append(list(c))

        response['result'] = 'Success'
        response['pairs'] = len(pairs)
    else:
        response['result'] = 'Failed'
    return make_response(jsonify(response))

@app.route('/api/template', methods=['GET'])
def get_template():
    # URLパラメータ
    response = {}
    global template
    global pairs
    global treat
    global similars_len

    try:
        pair = pairs.pop(0)
        treat += 1
        template_tmp = Template({"keys":pair})
        if template_tmp.select_similar():
            if len(template_tmp.similars) > similars_len:
                similars_len = len(template_tmp.similars)
                template = template_tmp

        if len(pair) > len(pairs[0]) and similars_len > 0:
            template.recommended_infobox()
            template.recommended_sections()
            response['result'] = 'Success'
            response['infobox'] = template.infobox.to_dict()
            response['sections'] = template.secs
            response['wiki'] = template.to_wiki()
            pairs = []
        else:
            response['result'] = 'Generating now'
            response['treat'] = treat
    except:
        response['result'] = 'Not found articles matching to keywords'

    return make_response(jsonify(response))

@app.route('/api/regenerate', methods=['GET'])
def regenerate_template():
    # URLパラメータ
    params = request.args
    response = {}
    keys = []
    global template

    if 'infobox' in params:
        ib_title = params.get('infobox')
        template.change_infobox(ib_title)
        template.recommended_sections()

        response['result'] = 'Success'
        response['infobox'] = template.infobox.to_dict()
        response['sections'] = template.secs
        response['wiki'] = template.to_wiki()
    else:
        response['result'] = 'Could not generate template'
    return make_response(jsonify(response))

@app.route('/api/similars', methods=['GET'])
def get_similars():
    global template
    response = {}
    response['similars'] = [{'ib_title': box['title'], 'similars': [{'title': s.title, 'sections': s.secs} for s in box['similars']]} for box in template.ib_similars]
    return make_response(jsonify(response))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
