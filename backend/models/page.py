# -*- coding: utf-8 -*-
from ..lib import accessor as ac
from ..lib.wiki_extractor import WikiExtractor as wiki
import json
import MeCab
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import collections
from math import log
import pandas as pd

class Page:
    """
    A superclass for Wikipedia Page
    """
    page_id = ac.reader("_page_id")
    title = ac.reader("_title")

    ext = wiki("settings.yml")
    c_d = {}

    def __init__(self, params):
        """
        param: dictionary of page info
        """

        self._page_id = params["page_id"]
        self._title = params["title"]

        try:
            cates = pd.DataFrame.from_dict(params["cates"])
        except KeyError:
            cates = []

        self._cates = cates

    def to_json(self):
        attrs = {}
        for attr in self.__dict__.items():
            if attr[0][1:] in ["page_id", "title", "cates"]:
                attrs[attr[0][1:]] = attr[1]
        return json.dumps(attrs, ensure_ascii=False, sort_keys=True)

    def categories(self):
        cates = []
        if len(self._cates) == 0:
            self._cates = self.__get_cates()

        for i, cate in self._cates.iterrows():
            c = Category({"page_id":cate["page_id"], "title":cate["page_title"], "src": [self.page_id]})
            cates.append(c)
        return cates

    # private methods
    def __get_cates(self):
        try:
            return self.c_d[self.page_id]
        except KeyError:
            self.c_d[self.page_id] = self.ext.categories(self.page_id)
            return self.c_d[self.page_id]

    def info(self):
        print("page_id: {}".format(self._page_id))
        print("title:   {}".format(self._title))

    @classmethod
    def from_json(cls, params):
        return cls(json.loads(params))


## Subclasses of Page and PageCollection ###########
class Article(Page):
    """
    A subclass of Page for Wikipedia articles
    """
    secs = ac.writer("_secs")
    infobox = ac.reader("_infobox")
    keywords = ac.writer("_keywords")
    tf = ac.reader("_tf")
    tfidf = ac.reader("_tfidf")
    target = ac.reader("_target")
    filtered = ac.reader("_filtered")

    alpha = 0.5
    c_d = {}
    df = {}

    def __init__(self, params):
        super().__init__(params)
        try:
            tf = params["tf"]
        except KeyError:
            tf = {}
        try:
            tfidf = params["tfidf"]
        except KeyError:
            # tfidf = self.tfidf_d[self.tfidf_d["page_id"] == self.page_id].iloc[0].tiidf
            tfidf = {}
        try:
            keys = params["keywords"]
        except KeyError:
            keys = []
        try:
            target = params["target"]
        except KeyError:
            target = ""

        self._secs = []
        self._infobox = params["infobox"]
        self._tf = tf
        self._tfidf = tfidf
        self._keywords = keys
        self._filtered = self.filtered_keys()
        self._target = target

    def to_json(self):
        attrs = {}
        for attr in self.__dict__.items():
            if attr[0][1:] in ["page_id", "title", "infobox", "secs", "tf", "tfidf", "keywords"]:
                attrs[attr[0][1:]] = attr[1]
            if attr[0][1:] == "cates":
                attrs[attr[0][1:]] = attr[1].to_dict(orient='records')
            if attr[0][1:] == "target":
                attrs[attr[0][1:]] = [{"title":c.title, "page_id":c.page_id} for c in attr[1]]
        return json.dumps(attrs, ensure_ascii=False, sort_keys=True)

    def get_target(self):
        l_1 = self.categories()
        l_2 = [cate for sub in [c.categories() for c in l_1] for cate in sub]
        all_targets = l_1 + l_2
        self._target = all_targets

    def calc_tf(self):
        if self._target == "":
            self.get_target()
        else:
            self._target = [Category(c) for c in self._target]

        candidates = [c.last_word() for c in self._target]
        counted = collections.Counter(candidates)
        tf = [(w[0], w[1]/len(candidates)) for w in counted.most_common()] # 頻出単語順に並べすべてをキーワードとして抽出
        for w in tf:
            try:
                self.df[w[0]] = self.df[w[0]] + 1
            except KeyError:
                self.df[w[0]] = 1
        self._tf = tf

    def extract_key(self, pages_n):
        tfidf = {}
        for w in self._tf:
            tfidf[w[0]] = self.__tfidf(w[1], self.df[w[0]], pages_n)

        sorted_tfidf = sorted(tfidf.items(), key=lambda x: -x[1])
        self._tfidf = tfidf
        self._keywords = [w[0] for w in sorted_tfidf]

    def filtered_keys(self):
        keys = []
        for key, value in self.tfidf.items():
            if value >= self.alpha:
                keys.append(key)

        return keys

    def __tfidf(self, TF, DF, N):
        return TF * log( N / DF )

    def save(self):
        self.ext.insert_article(self._page_id, self._title, self._infobox, self._keywords)

    @classmethod
    def from_df(cls, df):
        params = {"page_id":df.page_id, "title":df.title, "infobox":df.infobox}
        a = cls(params)
        a.keywords = eval(df.keywords)
        try:
            a.secs = eval(df.sections)
        except TypeError:
            a.secs = []
        return a

    @classmethod
    def read_tfidf(cls):
        cls.tfidf_d = pd.read_json(open("db/json/pro_all_tfidf_20180601.json", "r+"))


class Category(Page):
    """
    A subclass of Page for Wikipedia category
    """

    def __init__(self, params):
        super().__init__(params)

    def last_word(self):
        return self.__word_l()

    def __word_l(self):
        """
        Return tokens of category
        """
        a = Analyzer(token_filters=[CompoundNounFilter(),POSKeepFilter(['名詞'])])
        words = [token.surface for token in a.analyze(self._title)]
        if words:
            return words[-1]
        else:
            return ""
    #     m = MeCab.Tagger('mecabrc')
    #     m.parseToNode('')

    #     words =  [token for token in self.__tokenize(m)]
    #     if words:
    #         return words[-1]
    #     else:
    #         return ""

    # # private method
    # def __tokenize(self, m):
    #     node = m.parseToNode(self._title)
    #     while node:
    #         if node.feature.split(',')[0] == '名詞':
    #             yield node.surface.lower()
    #         node = node.next


class Infobox(Page):
    """
    A subclass of Page for Wikipedia template (ex. infobox)
    """
    arg = ac.reader("_arg")

    def __init__(self, params):
        super().__init__(params)
        try:
            arg = params["arg"]
        except KeyError:
            arg = []
        self._arg = arg # arguments for create infobox

    def to_wiki(self):
        """
        Output wiki template
        """
        html = "\{\{{}\}\}".format(self.title)
