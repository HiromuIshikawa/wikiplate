# -*- coding: utf-8 -*-
from backend.models.page import Article, Category
from backend.lib.wiki_extractor import WikiExtractor as wiki
import pandas as pd
import numpy as np
import yaml
import json
from ijson import parse
import sys

if __name__ == "__main__":

    ext = wiki('settings.yml')
    raw = open("db/json/pro_keyed_article_compound_20180601.json", "r+")
    parser = parse(raw)

    tfidf_01 = []
    tfidf_02 = []
    tfidf_03 = []
    tfidf_04 = []
    tfidf_06 = []
    tfidf_07 = []


    for prefix, event, value in parser:
        if (prefix, event) == ('item', 'string'):
            a = Article.from_json(value)
            df = pd.DataFrame(a.tfidf,index=[0])
            over_01 = df[df >= 0.1].dropna(how='all', axis=1).to_dict('records')[0]
            over_02 = df[df >= 0.2].dropna(how='all', axis=1).to_dict('records')[0]
            over_03 = df[df >= 0.3].dropna(how='all', axis=1).to_dict('records')[0]
            over_04 = df[df >= 0.4].dropna(how='all', axis=1).to_dict('records')[0]
            over_06 = df[df >= 0.6].dropna(how='all', axis=1).to_dict('records')[0]
            over_07 = df[df >= 0.7].dropna(how='all', axis=1).to_dict('records')[0]

            tfidf_01.append({"page_id":a.page_id, "tiidf":over_01})
            tfidf_02.append({"page_id":a.page_id, "tiidf":over_02})
            tfidf_03.append({"page_id":a.page_id, "tiidf":over_03})
            tfidf_04.append({"page_id":a.page_id, "tiidf":over_04})
            tfidf_06.append({"page_id":a.page_id, "tiidf":over_06})
            tfidf_07.append({"page_id":a.page_id, "tiidf":over_07})
            # a.save()
            # "ext.add_comp_keywords(a.page_id, a.keywords)
            print("add_key {}".format(a.title))

    out01 = open("db/json/pro_all_tfidf_compound_over_01_20180601.json","w")
    json.dump(tfidf_01, out01, ensure_ascii=False)
    out01.close()

    out02 = open("db/json/pro_all_tfidf_compound_over_02_20180601.json","w")
    json.dump(tfidf_02, out02, ensure_ascii=False)
    out02.close()

    out03 = open("db/json/pro_all_tfidf_compound_over_03_20180601.json","w")
    json.dump(tfidf_03, out03, ensure_ascii=False)
    out03.close()

    out04 = open("db/json/pro_all_tfidf_compound_over_04_20180601.json","w")
    json.dump(tfidf_04, out04, ensure_ascii=False)
    out04.close()

    out06 = open("db/json/pro_all_tfidf_compound_over_06_20180601.json","w")
    json.dump(tfidf_06, out06, ensure_ascii=False)
    out06.close()

    out07 = open("db/json/pro_all_tfidf_compound_over_07_20180601.json","w")
    json.dump(tfidf_07, out07, ensure_ascii=False)
    out07.close()

    raw.close()
