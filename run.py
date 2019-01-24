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

sessions = []
session_num = 0

@app.route('/api/pairs', methods=['GET'])
def get_pairs():
    # URLパラメータ
    params = request.args
    response = {}
    keys = []
    global sessions
    global session_num
    pairs = []


    if 'keywords' in params:
        keys = params.get('keywords').split(":")
        print(keys)
        for key_num in reversed(range(len(keys) + 1)[1:]):
            print("キーワード数 {} の組合せ".format(key_num))
            for c in combinations(keys, key_num):
                pairs.append(list(c))

        response['result'] = 'Success'
        response['pairs'] = len(pairs)
        response['session'] = session_num
        session_num += 1
        sessions.append({'pairs': pairs, 'treat': 0, 'similars_len': 0})
    else:
        response['result'] = 'Failed'
    return make_response(jsonify(response))

@app.route('/api/template', methods=['GET'])
def get_template():
    # URLパラメータ
    params = request.args
    response = {}

    global sessions
    s = int(params.get('session'))
    print(s)
    print(sessions[s])

    try:
        pair = sessions[s]['pairs'].pop(0)
    except:
        pair = ""
    if pair != "":
        sessions[s]['treat'] += 1
        template_tmp = Template({"keys":pair})
        if template_tmp.select_similar():
            if len(template_tmp.similars) > sessions[s]['similars_len']:
                sessions[s]['similars_len'] = len(template_tmp.similars)
                sessions[s]['template'] = template_tmp
                sessions[s]['selected_pair'] = pair

        try:
            next_p = sessions[s]['pairs'][0]
        except:
            next_p = []

        if len(pair) > len(next_p) and sessions[s]['similars_len'] > 0:
            sessions[s]['template'].recommended_infobox()
            sessions[s]['template'].recommended_sections()
            print(sessions[s])
            response['result'] = 'Success'
            response['infobox'] = sessions[s]['template'].infobox.to_dict()
            response['sections'] = sessions[s]['template'].secs
            response['wiki'] = sessions[s]['template'].to_wiki()
            response['keywords'] = sessions[s]['selected_pair']
        else:
            response['result'] = 'Generating now'
            response['treat'] = sessions[s]['treat']
    else:
        response['result'] = 'Not found articles matching to keywords'

    return make_response(jsonify(response))

@app.route('/api/regenerate', methods=['GET'])
def regenerate_template():
    # URLパラメータ
    params = request.args
    response = {}

    global sessions
    s = int(params.get('session'))

    if 'infobox' in params:
        ib_title = params.get('infobox')
        sessions[s]['template'].change_infobox(ib_title)
        sessions[s]['template'].recommended_sections()

        response['result'] = 'Success'
        response['infobox'] = sessions[s]['template'].infobox.to_dict()
        response['sections'] = sessions[s]['template'].secs
        response['wiki'] = sessions[s]['template'].to_wiki()
        response['keywords'] = sessions[s]['selected_pair']
    else:
        response['result'] = 'Could not generate template'
    return make_response(jsonify(response))

@app.route('/api/similars', methods=['GET'])
def get_similars():
    params = request.args
    response = {}

    global sessions
    s = int(params.get('session'))

    response['similars'] = [{'ib_title': box['title'], 'similars': [{'title': s.title, 'sections': s.secs} for s in box['similars']]} for box in sessions[s]['template'].ib_similars]
    return make_response(jsonify(response))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
