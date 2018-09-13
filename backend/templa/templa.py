# -*- coding: utf-8 -*-
from ..lib.wiki_extractor import WikiExtractor as wiki
from ..models.page import Article
from ..lib import accessor as ac

class Templa:
    """
    class for Templa
    """
    ext = wiki("settings.yml")

    title = ac.reader("_title")
    keys = ac.reader("_keys")
    secs = ac.reader("_secs")
    infobox = ac.reader("_infobox")
    similars = ac.reader("_similars")

    def __init__(self, params):
        self._title = params["title"]
        self._keys = params["keys"]
        self._secs = []
        self._infobox = []
        self._similars = []

    def select_similar(self):
        similar_df = self.ext.articles_from_keys(self.keys)
        self._similars = [Article.from_df(row) for i, row in similar_df.iterrows()]
        print("{} similars are extracted")

    def reccomended_infobox(self):
        pass

    def to_wiki(self):
        pass
