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
        for key_num in reversed(range(len(keys) + 1)[1:]):
            pairs = []
            selected = ""
            similars_len = 0
            print("キーワード数 {} の組合せ".format(key_num))
            for c in combinations(keys, key_num):
                pairs.append(c)
            for p in pairs:
                print(p)
                template = Template({"keys":list(p)})
                if template.select_similar():
                    if len(template.similars) > similars_len:
                        similars_len = len(template.similars)
                        selected = template
                        selected_keys = list(p)
            if similars_len > 0:
                print("found simialrs!!")
                break

        if selected != "":
            template = selected
        else:
            template = ""

    if template != "":
        template.recommended_infobox()
        template.recommended_sections()

        response['result'] = 'Success'
        response['infobox'] = template.infobox.to_dict()
        response['sections'] = template.secs
        response['wiki'] = template.to_wiki()
    else:
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
