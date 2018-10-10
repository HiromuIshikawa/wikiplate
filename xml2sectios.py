# -*- coding: utf-8 -*-
from lxml import etree
import re
import json

if __name__ == "__main__":

    # tree = etree.parse('db/dump/test.xml')
    tree = etree.parse('db/dump/jawiki-20180601-pages-articles.xml')
    root = tree.getroot()

    output = []
    for page in root.findall('./page', root.nsmap):
        if page.find('./ns', root.nsmap).text == '0':
            page_id = int(page.find('./id', root.nsmap).text)
            print("{}: {}".format(page.find('./id', root.nsmap).text, page.find('./title', root.nsmap).text))
            content = page.find('./revision', root.nsmap).find('./text', root.nsmap).text
            sections = re.findall('[^=]== (.+) ==[^=]', content)
            output.append({"page_id":page_id, "sections":sections})
    dest = open("db/json/all_sections_20180601.json","w")
    json.dump(output, dest, ensure_ascii=False)
    dest.close()
