# -*- coding: utf-8 -*-
from backend.models.page import Article
from backend.lib.wiki_extractor import WikiExtractor as wiki
import pandas as pd
import numpy as np
import sys

if __name__ == "__main__":

    params = sys.argv
    ext = wiki("settings.yml")
    Article.read_tfidf()
    titles = params[1].split(",")
    articles = [Article.from_df(df) for i,df in ext.articles_from_titles(titles).iterrows()]
    for a in articles:
        print(a.title, ":", a.secs)
