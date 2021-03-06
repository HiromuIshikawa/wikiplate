# -*- coding: utf-8 -*-
from ..lib import accessor as ac
from ..lib.wiki_extractor import WikiExtractor as wiki
import json
# from janome.tokenizer import Tokenizer
# from janome.analyzer import Analyzer
# from janome.charfilter import *
# from janome.tokenfilter import *
import collections
from math import log
import pandas as pd
import functools

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
    tfidf_d = pd.DataFrame()
    alpha = 0.5
    c_d = {}
    df = {}

    def __init__(self, params):
        super().__init__(params)
        # try:
        #     tf = params["tf"]
        # except KeyError:
        #     tf = {}
        # try:
        #     tfidf = params["tfidf"]
        # except KeyError:
        #     tfidf = self.tfidf_all[self.tfidf_all["page_id"] == self.page_id].iloc[0].tiidf
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
        # self._tf = tf
        # self._tfidf = tfidf
        self._keywords = keys
        # self._filtered = self.filtered_keys()
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

    # def calc_tf(self):
    #     if self._target == "":
    #         self.get_target()
    #     else:
    #         self._target = [Category(c) for c in self._target]

    #     candidates = [c.last_word() for c in self._target]
    #     counted = collections.Counter(candidates)
    #     tf = [(w[0], w[1]/len(candidates)) for w in counted.most_common()] # 頻出単語順に並べすべてをキーワードとして抽出
    #     for w in tf:
    #         try:
    #             self.df[w[0]] = self.df[w[0]] + 1
    #         except KeyError:
    #             self.df[w[0]] = 1
    #     self._tf = tf

    # def extract_key(self, pages_n):
    #     tfidf = {}
    #     for w in self._tf:
    #         tfidf[w[0]] = self.__tfidf(w[1], self.df[w[0]], pages_n)

    #     sorted_tfidf = sorted(tfidf.items(), key=lambda x: -x[1])
    #     self._tfidf = tfidf
    #     self._keywords = [w[0] for w in sorted_tfidf]

    def filtered_keys(self):
        keys = []
        for key, value in self.tfidf.items():
            if value >= self.alpha:
                keys.append(key)

        return keys

    # def __tfidf(self, TF, DF, N):
    #     return TF * log( N / DF )

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
    def from_keys(cls, keys):
        # if cls.tfidf_d.empty:
        #     cls.read_tfidf()

        # d = cls.tfidf_d
        # target_ids = []
        ##### When use filtered tfidf file, use bellow code
        # target_ids = list(functools.reduce(lambda x, y: x & y, [set(d[d[0] == key].page_id.values) for key in keys]))
        ##### When use not filtered tfidf file by alpha(>= 0.5), use bellow code
        # for i, row in d.iterrows():
        #     if row.tiidf.keys() >= set(keys):
        #         if functools.reduce(lambda x, y: x and y, [row.tiidf[key] >= cls.alpha for key in keys]):
        #             target_ids.append(row.page_id)
        similars_df = cls.ext.articles_from_keys(keys)
        if similars_df.empty:
            return False
        else:
            return [cls.from_df(df) for i, df in similars_df.iterrows()]


    @classmethod
    def read_tfidf(cls):
        src = open("db/json/pro_all_tfidf_compound_over_24_20180601.json", "r+") # 閾値ごとにファイルがわれている．ex) over_01 -> α>=0.1
        src_all = open("db/json/pro_all_tfidf_compound_20180601.json", "r+")
        js = json.load(src)
        src.close()
        cls.tfidf_d = pd.io.json.json_normalize(js,'tiidf',['page_id'])
        cls.tfidf_all = pd.read_json(src_all)
        print("read tfidf and keywords dictionary.")

class Category(Page):
    """
    A subclass of Page for Wikipedia category
    """

    def __init__(self, params):
        super().__init__(params)

    # def last_word(self):
    #     return self.__word_l()

    # def __word_l(self):
    #     """
    #     Return tokens of category
    #     """
    #     # janome version
    #     # a = Analyzer(token_filters=[CompoundNounFilter(),POSKeepFilter(['名詞'])])
    #     # words = [token.surface for token in a.analyze(self._title)]
    #     # if words:
    #     #     return words[-1]
    #     # else:
    #     #     return ""
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
    #     compound = ""
    #     while node:
    #         if node.feature.split(',')[0] == '名詞':
    #             compound += node.surface.lower()
    #         else:
    #             if compound != "":
    #                 yield compound
    #                 compound = ""
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

        try:
            url = params["url"]
        except KeyError:
            url = ""

        self._arg = arg # arguments for create infobox
        self._url = url

    def to_dict(self):
        return {'title': self._title, 'arg': self._arg, 'url': self._url}

    def to_wiki(self):
        """
        Output wiki template
        """
        wiki =  "{{" + " {} ".format(self._title) + "\n"
        for a in self._arg:
            wiki += "|{} = \n".format(a)

        wiki += "}}\n\n"

        return wiki
