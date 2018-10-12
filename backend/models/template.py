# -*- coding: utf-8 -*-
from ..lib.wiki_extractor import WikiExtractor as wiki
from .page import Article, Infobox
from .sections_graph import SectionsGraph as sg
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

    # When get articles by not compound keys, use bellow code
    # def select_similar(self):
    #     df = self.ext.articles_from_keys(self.keys)
    #     candidates = [Article.from_df(row) for i, row in df.iterrows()]
    #     similars = [a for a in candidates if self.__judge_key(a)]
    #     self._similars = similars
    #     print("{} similars are extracted".format(len(self._similars)))

    def select_similar(self):
        similars = Article.from_keys(self.keys)
        if similars:
            self._similars = similars
            print("{} similars are extracted".format(len(self._similars)))
            return True
        else:
            print("Not found articles matching to keywords")
            return False

    def recommended_infobox(self): # TODO: get params of infobox by using wikipedia api client
        infobox_candidates = [a.infobox for a in self._similars]
        counted_infobox = Counter(infobox_candidates)
        common_infobox_id = counted_infobox.most_common(1)[0][0]
        infobox_df = self.ext.page(common_infobox_id).iloc[0]
        self._infobox.append(Infobox({"page_id": infobox_df.page_id, "title": infobox_df.page_title}))

    def recommended_sections(self):
        graph = sg()
        for a in self._similars:
            graph.add_sections(a.secs)
        graph.create_djacency()
        self._secs = graph.dijkstra_path()

    def to_wiki(self):
        pass

    def __judge_key(self, a): # 入力されたキーワードの全てが，閾値以上の特徴語に含まれるかを判断
        return list(set(self._keys) & set(a.filtered)).sort() == self.keys.sort()
