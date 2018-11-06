# -*- coding: utf-8 -*-
from backend.models.template import Template
from backend.models.page import Article
import pandas as pd
import numpy as np
import sys

if __name__ == "__main__":

    params = sys.argv
    Article.read_tfidf()
    while 1:
        line = input("input keywords: ")
        if line == "quit":
            print("bye...")
            break
        else:
            params = line.split(":")
            keys = params[0].split(",")
            template = Template({"title":"test_article", "keys":keys})

            if template.select_similar():

                template.recommended_infobox()
                print("Infobox: '{}'".format(template.infobox.title))
                template.recommended_sections()
                print("Section: {}".format(template.secs))
                try:
                    if params[1] == "title":
                        for p in template.similars:
                            print(p.title)
                    elif params[1] == "sections":
                        for p in template.similars:
                            print(p.secs)
                    elif params[1] == "wiki":
                        print(template.to_wiki())
                except:
                    pass
