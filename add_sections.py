# -*- coding: utf-8 -*-
from lxml import etree
import re
import json
from backend.models.page import Article
from backend.lib.wiki_extractor import WikiExtractor as wiki
import pandas as pd
import numpy as np

if __name__ == "__main__":

    ns = {'wiki': 'http://www.mediawiki.org/xml/export-0.10/'}
    ext = wiki('settings.yml')
    print("reading xml...", end="", flush=True)
    # tree = etree.parse('db/dump/test.xml')
    tree = etree.parse('db/dump/jawiki-20180601-pages-articles.xml')
    print("    complete.")
    root = tree.getroot()
    print("reading all Articles from MySQL...", end="", flush=True)
    articles = ext.articles()
    print("    complete.")
    ids = articles.page_id.values

    for page in root.xpath('./wiki:page', namespaces=ns):
        page_id = int(page.xpath('./wiki:id', namespaces=ns)[0].text)
        if page_id in ids:
            title = page.xpath('./wiki:title', namespaces=ns)[0].text
            content = page.xpath('./wiki:revision/wiki:text', namespaces=ns)[0].text
            sections = list(map(lambda x:x.replace(" ",""), re.findall('[^=]==([^=]+)==[^=]',content)))
            ext.add_sections(page_id, sections)
