# -*- coding: utf-8 -*-
from backend.lib.wiki_extractor import WikiExtractor as wiki
from backend.models.page import Article
import pandas as pd
import numpy as np
import yaml
import json

if __name__ == "__main__":
    f = "settings.yml"

    sorted_ib = pd.read_csv("db/csv/infobox_linked_count_20180601.csv").sort_values(by=["linked_count"], ascending=False)[5:]
    # mode_ib = sorted_ib[sorted_ib.linked_count >= 100]
    mode_ib = sorted_ib[:10]
    print(mode_ib)
    target_ib = [row.page_title for i, row in mode_ib.iterrows()]
    len(target_ib)
    #############################

    raw = open("db/json/infobox_20180601.json", "r+")
    conf = yaml.load(f)
    ext = wiki(conf)

    infoboxies = json.load(raw)
    articles = []
    for box in infoboxies[5:15]:
        print(box)
        dict_box = json.loads(box)
        if dict_box["title"] in target_ib:
            print("Get articles boxed by " + dict_box["title"])
            pages = ext.infoboxed_pages(dict_box["title"])
            for i, p in pages.iterrows():
                article = Article({"page_id":p.page_id, "title": p.page_title, "secs":[], "infobox": dict_box["page_id"]})
                print(article.title)
                js = article.to_json()
                print(js)
                articles.append(js)

    out = open("../json/top_10_boxed_article_20180601.json","w")
    json.dump(articles, out, ensure_ascii=False)

    raw.close()
    out.close()
    ext.close()
