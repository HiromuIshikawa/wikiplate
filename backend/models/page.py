# -*- coding: utf-8 -*-
from ..lib import accessor as ac
from ..lib.wiki_extractor import WikiExtractor as wiki
import json
import MeCab
import collections
from math import log

class Page:
    """
    A superclass for Wikipedia Page
    """
    page_id = ac.reader("_page_id")
    title = ac.reader("_title")

    ext = wiki("settings.yml")

    def __init__(self, params):
        """
        param: dictionary of page info
        """
        self._page_id = params["page_id"]
        self._title = params["title"]
        self._cates = self.__get_cates()

    def to_json(self):
        attrs = {}
        for attr in self.__dict__.items():
            if attr[0][1:] in ["page_id", "title"]:
                attrs[attr[0][1:]] = attr[1]
        return json.dumps(attrs, ensure_ascii=False, sort_keys=True)

    def categories(self):
        cates = []
        for i, cate in self._cates.iterrows():
            c = Category({"page_id":cate["page_id"], "title":cate["page_title"], "src": [self.page_id]})
            cates.append(c)
        return cates

    # private methods
    def __get_cates(self):
        return self.ext.categories(self.page_id)

    @classmethod
    def from_json(cls, params):
        print(params)
        return cls(json.loads(params))


## Subclasses of Page and PageCollection ###########
class Article(Page):
    """
    A subclass of Page for Wikipedia articles
    """
    secs = ac.reader("_secs")
    infobox = ac.reader("_infobox")
    keywords = ac.writer("_keywords")

    df = {}

    def __init__(self, params):
        super().__init__(params)
        self._secs = params["secs"]
        self._infobox = params["infobox"]
        self._tf = {}
        self._keywords = [""]

    def to_json(self):
        attrs = {}
        for attr in self.__dict__.items():
            if attr[0][1:] in ["page_id", "title", "infobox", "secs"]:
                attrs[attr[0][1:]] = attr[1]
        return json.dumps(attrs, ensure_ascii=False, sort_keys=True)

    def calc_tf(self):
        l_1 = self.categories()
        l_2 = [cate for sub in [c.categories() for c in l_1] for cate in sub]
        all_targets = l_1 + l_2

        candidates = [c.last_word for c in all_targets]
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
        self._keywords = [w[0] for w in sorted_tfidf[:5]]

    def __tfidf(self, TF, DF, N):
        return TF * log( N / DF )

    def save(self):
        self.ext.insert_article(self._page_id, self._title, self._infobox, self._keywords)

    @classmethod
    def from_df(cls, df):
        params = {"page_id":df.page_id, "title":df.title, "infobox":df.infobox, "secs":[]}
        a = cls(params)
        a.keywords = df.keywords
        return a


class Category(Page):
    """
    A subclass of Page for Wikipedia category
    """
    last_word = ac.reader("_last_word")

    def __init__(self, params):
        super().__init__(params)
        self._last_word = self.__word_l()

    def __word_l(self):
        """
        Return tokens of category
        """
        m = MeCab.Tagger('mecabrc')
        m.parseToNode('')

        words =  [token for token in self.__tokenize(m)]
        if words:
            return words[-1]
        else:
            return ""

    # private method
    def __tokenize(self, m):
        node = m.parseToNode(self._title)
        while node:
            if node.feature.split(',')[0] == '名詞':
                yield node.surface.lower()
            node = node.next


class Infobox(Page):
    """
    A subclass of Page for Wikipedia template (ex. infobox)
    """
    arg = ac.reader("_arg")

    def __init__(self, params):
        super().__init__(params)

        self._arg = params["arg"] # arguments for create infobox

    def to_html(self):
        """
        Output html template
        """
        html = "\{\{{}\}\}".format(self.title)
