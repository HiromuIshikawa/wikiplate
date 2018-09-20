# -*- coding: utf-8 -*-
from backend.models.page import Article, Category
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml
import json
import sys
import collections

if __name__ == "__main__":

    raw = open("db/json/pro_boxed_article_20180601.json", "r+")
    articles_json = json.load(raw)
    print(len(articles_json))
    articles = [Article.from_json(json) for json in articles_json]

    out_data = []

    for a in articles:
        a.get_target()
        js = a.to_json()
        print(a.title)
        out_data.append(js)

    out = open("db/json/pro_cated_article_20180601.json","w")
    json.dump(out_data, out, ensure_ascii=False)
    out.close()

    raw.close()
