# -*- coding: utf-8 -*-
from ..lib.wiki_extractor import WikiExtractor as wiki
from .page import Article, Infobox
from .sections_graph import SectionsGraph as sg
from ..lib import accessor as ac
from collections import Counter
import wikipedia as wk
import re

class Template:
    """
    class for Template
    """
    ext = wiki("settings.yml")

    keys = ac.reader("_keys")
    secs = ac.reader("_secs")
    infobox = ac.reader("_infobox")
    similars = ac.reader("_similars")
    ib_similars = ac.reader("_ib_similars")

    def __init__(self, params):
        self._keys = params["keys"]
        self._secs = []
        self._infobox = ""
        self._similars = []
        self._ib_similars = []

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
            similars = [s for s in similars if len(s.secs) > 4] # 質の低い(章項目の少ない)記事による，章構成への影響をなくすため．5以上の条件は感覚で決めたもの．
            if len(similars) > 0:
                self._similars = similars
            else:
                print("Not found articles matching to keywords")
                return False

            print("{} similars are extracted".format(len(self._similars)))
            return True
        else:
            print("Not found articles matching to keywords")
            return False

    def recommended_infobox(self): # TODO: get params of infobox by using wikipedia api client
        infobox_candidates = [a.infobox for a in self._similars]
        counted_infobox = Counter(infobox_candidates).most_common()
        arg = []
        for ib in counted_infobox:
            ib_df = self.ext.page(ib[0]).iloc[0]
            similars = [s for s in self._similars if s.infobox == ib_df.page_id]
            self._ib_similars.append({'page_id': ib_df.page_id, 'title': ib_df.page_title, 'similars': similars})

        # for (i,ib) in enumerate(self._ib_candidate):
        #     print(ib)
        #     arg = self.__get_args(ib['title'])

        selected = self._ib_similars[0]
        arg = self.__get_args(selected['title'])
        url = "https://ja.wikipedia.org/wiki/Template:" + selected['title']
        self._infobox = (Infobox({"page_id": selected['page_id'], "title": selected['title'], "arg": arg, "url": url}))

    def change_infobox(self, title):
        for ib in self._ib_similars:
            if ib['title'] == title:
                arg = self.__get_args(title)
                url = "https://ja.wikipedia.org/wiki/Template:" + title
                self._infobox = (Infobox({"page_id": ib['page_id'], "title": ib['title'], "arg": arg, "url": url}))

    def recommended_sections(self):
        graph = sg()
        target = [ib['similars'] for ib in self._ib_similars if ib['page_id'] == self._infobox.page_id][0]
        for a in target:
            # print(a.title, ":", a.secs)
            graph.add_sections(a.secs)
        graph.create_djacency()
        self._secs = graph.dijkstra_path()

    def ib_title(self, page_id):
        for ib in self._ib_similars:
            if page_id == ib['page_id']:
                return ib['title']

        return 'unknown'

    def to_wiki(self):
        sections = ""
        for sec in self._secs:
            sections = sections + "== {} ==\n\n".format(sec)

        info_wiki = self._infobox.to_wiki()
        return info_wiki + sections

    def __get_args(self, title):
        wk.set_lang("ja")
        query = "Template:" + title + "/doc"
        try:
            page = wk.page(query)
        except:
            print("not found doc page for {}".format(title))
            return []

        print(title)
        usage = page.section("使い方")
        if not usage:
            usage = page.section("使用法")
        if not usage:
            usage = page.section('コード')
        if usage:
            arg = re.findall('\|(.+) *=', usage)
            return arg
        return []

    def __judge_key(self, a): # 入力されたキーワードの全てが，閾値以上の特徴語に含まれるかを判断
        return list(set(self._keys) & set(a.filtered)).sort() == self.keys.sort()
