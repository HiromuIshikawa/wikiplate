# -*- coding: utf-8 -*-
from backend.models.page import Article, Category
import pandas as pd
import numpy as np
import yaml
import json
import sys
import collections

if __name__ == "__main__":

    raw = open("db/json/pro_cated_article_20180601.json", "r+")
    articles_json = json.load(raw)
    print(len(articles_json))
    articles = [Article.from_json(json) for json in articles_json]

    for a in articles:
        print(a.title)
        a.calc_tf()

    out_data = []
    for a in articles:
        a.extract_key(len(articles))
        js = a.to_json()
        out_data.append(js)
        print("{}: {}".format(a.title, a.keywords))

    out = open("db/json/pro_keyed_article_compound_20180601.json","w")
    json.dump(out_data, out, ensure_ascii=False)

    out.close()
    raw.close()
