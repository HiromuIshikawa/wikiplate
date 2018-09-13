# -*- coding: utf-8 -*-
from backend.models.page import Article, Category
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml
import json
import sys
import collections
import matplotlib
font = {'family': 'IPAPGothic'}
matplotlib.rc('font', **font)
plt.style.use('seaborn-talk')
plt.style.use("ggplot")

def true_rate(articles):

    result = [judge(a) for a in articles]
    rate = result.count(True)
    return rate

def judge(a):
    keys = {320720:["企業","会社"], 1757819:["俳優","女優","役者"], 818626:["音楽家","ミュージシャン","バンド","歌手"], 758910:["シングル","楽曲"], 266218:["アルバム"]}

    if set(a.keywords) & set(keys[a.infobox]):
        return True
    else:
        return False

if __name__ == "__main__":

    raw = open("db/json/top_5_boxed_article_20180601.json", "r+")
    articles_json = json.load(raw)
    print(len(articles_json))
    articles = [Article.from_json(json) for json in articles_json]

    last_w_key = 0

    for a in articles:
        print(a.title)
        a.calc_tf()

    for a in articles:
        a.extract_key(len(articles))
        a.save()
        print("{}: {}".format(a.title, a.keywords))



    result = true_rate(articles)
    print(result)
    print("##################会社")
    result1 = true_rate(articles[:200])
    print(result1)

    print("##################俳優")
    result2 = true_rate(articles[200:400])
    print(result2)

    print("##################ミュージシャン")
    result3 = true_rate(articles[400:600])
    print(result3)

    print("##################アルバム")
    result4 = true_rate(articles[600:800])
    print(result4)

    print("##################シングル")
    result5 = true_rate(articles[800:1000])
    print(result5)

    # df = pd.DataFrame({"基礎情報_会社": result1,
    #                    "ActorActress": result2,
    #                    "Infobox_Musician": result3,
    #                    "Infobox_Album": result4,
    #                    "Infobox_Single": result5} ,index=["1", "2", "3", "4", "5"])


    # print(df)
    # ax = df.plot(kind="bar", grid=True, stacked=True)
    # bars = ax.patches
    # hatches = ''.join(h*len(df) for h in 'x.+/o')

    # for bar, hatch in zip(bars, hatches):
    #     bar.set_hatch(hatch)

    # ax.legend(loc='upper right', bbox_to_anchor=(1, 1))
    # ax.set_xlabel("対象の階層数(n)", fontsize=18)
    # ax.set_ylabel("正しいキーワードを抽出できた記事数", fontsize=20)
    # ax.xaxis.label.set_color('black')
    # ax.yaxis.label.set_color('black')
    # plt.show()
    raw.close()
