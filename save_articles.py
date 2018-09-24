# -*- coding: utf-8 -*-
from backend.models.page import Article, Category
import pandas as pd
import numpy as np
import yaml
import json
from ijson import parse
import sys

if __name__ == "__main__":

    raw = open("db/json/pro_keyed_article_20180601.json", "r+")
    parser = parse(raw)

    all_tfidf = []

    for prefix, event, value in parser:
        if (prefix, event) == ('item', 'string'):
            a = Article.from_json(value)
            all_tfidf.append({"page_id":a.page_id, "tiidf":a.tfidf})
            a.save()
            print("saveed {}".format(a.title))



    out = open("db/json/pro_all_tfidf_20180601.json","w")
    json.dump(all_tfidf, out, ensure_ascii=False)
    out.close()
    raw.close()
