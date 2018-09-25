# -*- coding: utf-8 -*-
from backend.templa.templa import Templa
from backend.models.page import Article, Category
from backend.lib.wiki_extractor import WikiExtractor as wiki
import matplotlib.pyplot as plt
import matplotlib
import json
import pandas as pd
import numpy as np
import sys
font = {'family': 'IPAPGothic'}
matplotlib.rc('font', **font)
plt.style.use('seaborn-talk')
# plt.style.use("ggplot")

def keywords(tfidf, alpha):
    keys = []
    for key, value in tfidf.items():
        if value >= alpha:
            keys.append(key)

    return keys

def evaluate(articles, tfidf_d, alpha, hit):
    judge_l = []
    prec_l = np.empty(200)
    all_keys = 0

    for i, a in enumerate(articles):
        tfidf = tfidf_d[tfidf_d["page_id"] == a.page_id].iloc[0].tiidf # caution: ファイル書き出し時点で tfidf -> tiidf のtypo 有
        keys = keywords(tfidf, alpha)
        all_keys += len(keys)
        judge_l.append(judge(keys, hit))
        prec_l[i] = precision(keys, hit)

    rate = judge_l.count(True)
    mean_prec = np.mean(prec_l)

    # return {"alpha": alpha, "rate": rate, "mean_prec": mean_prec}
    return all_keys

def judge(keys, hit):
    if set(keys) & set(hit):
        return True
    else:
        return False

def precision(keys, hit):
    try:
        return len(set(keys) & set(hit))/len(keys)
    except:
        return 0.0

def plot_result(df):
    ax1 = df.plot(kind="bar",color=['white', 'black'], edgecolor='black', x="alpha", secondary_y=["mean_prec"], linewidth=2)
    ax2 = ax1.right_ax

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()

    ax1.legend(h1+h2, ["正解のキーワードを抽出できた記事数", '適合率の平均(right)'], loc='lower left', bbox_to_anchor=(0, 1.01))
    ax1.set_xlabel("alpha", fontsize=20)
    ax1.set_ylabel("正解のキーワードを抽出できた記事数", fontsize=20)
    ax1.set_yticks([0,20,40,60,80,100,120,140,160,180,200])
    ax1.set_ylim(0,200)
    ax2.set_ylabel('適合率の平均', fontsize=20)
    ax2.set_yticks([round(0.10 * x,1) for x in range(11)])
    ax1.xaxis.label.set_color('black')
    ax1.yaxis.label.set_color('black')
    ax1.yaxis.grid(True, which = 'major', linestyle = '-', color = '#CFCFCF')
    ax1.set_axisbelow(True)
    plt.show()

if __name__ == "__main__":

    ext = wiki("settings.yml")

    raw = open("db/json/top_5_boxed_article_20180601.json", "r+")
    tfidf_raw = open("db/json/pro_all_tfidf_20180601.json", "r+")
    articles_json = json.load(raw)
    tfidf_d = pd.read_json(tfidf_raw)

    titles = {320720:"基礎情報_会社",
              1757819:"ActorActress",
              818626:"Infobox_Musician",
              758910:"Infobox_Single",
              266218:"Infobox_Album"}
    hits = {320720:["企業","会社"],
            1757819:["俳優","女優","役者"],
            818626:["音楽家","ミュージシャン","バンド","歌手"],
            758910:["シングル","楽曲"],
            266218:["アルバム"]}
    articles = {320720:[], 1757819:[], 818626:[], 758910:[], 266218:[]}
    results = {320720:[], 1757819:[], 818626:[], 758910:[], 266218:[]}

    print(len(articles_json))
    for js in articles_json:
        data = json.loads(js)
        page_id = data["page_id"]
        ib = data["infobox"]
        df = ext.article_from_id(page_id)
        a = Article.from_df(df[df["infobox"] == ib].iloc[0])
        try:
            articles[a.infobox].append(a)
        except:
            pass
            print(a.title)
            print(ext.page(a.infobox))

    all_key = [[0.0,0],[0.1,0],[0.2,0],[0.3,0],[0.4,0],[0.5,0],[0.6,0],[0.7,0],[0.8,0],[0.9,0],[1.0,0]]
    for key, value in articles.items():
        print("########## Infobox: {}".format(key))
        for alpha in [round(0.10 * x,1) for x in range(11)]:
            result = evaluate(value, tfidf_d, alpha, hits[key])
            for l in all_key:
                if l[0] == alpha:
                    l[1] += result
            results[key].append(result)
            print(result)

        # plot_result(pd.DataFrame(results[key]))

    r = []
    for value in all_key:
        r.append({"alpha":value[0], "keyword_num":value[1]/1000})
    r_df = pd.DataFrame(r)

    print(r_df)

    ax1 = r_df.plot(kind="bar",color=['black'], edgecolor='black', x="alpha", y=["keyword_num"], linewidth=2)

    h1, l1 = ax1.get_legend_handles_labels()

    ax1.legend(h1, ["選出される特徴語数の平均"], loc='lower left', bbox_to_anchor=(0, 1.01))
    ax1.set_xlabel("alpha", fontsize=20)
    ax1.set_ylabel("選出される特徴語数の平均", fontsize=20)
    ax1.xaxis.label.set_color('black')
    ax1.yaxis.label.set_color('black')
    ax1.yaxis.grid(True, which = 'major', linestyle = '-', color = '#CFCFCF')
    ax1.set_axisbelow(True)
    plt.show()

    raw.close()
    tfidf_raw.close()
