# -*- coding: utf-8 -*-
from ..lib.wiki_extractor import WikiExtractor as wiki
from .models.page import Article
from ..lib import accessor as ac
from collections import Counter

class Template:
    """
    class for Template
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
        df = self.ext.articles_from_keys(self.keys)
        candidates = [Article.from_df(row) for i, row in df.iterrows()]
        print(len(candidates))
        similars = [a for a in candidates if self.__judge_key(a)]
        self._similars = similars
        print("{} similars are extracted".format(len(self._similars)))

    def reccomended_infobox(self):
        infobox_candidates = [a.infobox for a in self._similars]
        counted_infobox = Counter(infobox_candidates)
        print(counted_infobox)

    def to_wiki(self):
        pass

    def __judge_key(self, a): # 入力されたキーワードの全てが，閾値以上の特徴語に含まれるかを判断
        return list(set(self._keys) & set(a.filtered)).sort() == self.keys.sort()
