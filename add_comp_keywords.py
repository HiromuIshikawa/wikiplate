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

    all_tfidf = []

    for prefix, event, value in parser:
        if (prefix, event) == ('item', 'string'):
            a = Article.from_json(value)
            df = pd.DataFrame(a.tfidf,index=[0])
            over_alpha = df[df >= 0.5].dropna(how='all', axis=1).to_dict('records')[0]
            all_tfidf.append({"page_id":a.page_id, "tiidf":over_alpha})
            # a.save()
            # "ext.add_comp_keywords(a.page_id, a.keywords)
            print("add_key {}".format(a.title))

    out = open("db/json/pro_all_tfidf_compound_over_alpha_20180601.json","w")
    json.dump(all_tfidf, out, ensure_ascii=False)
    out.close()
    raw.close()
