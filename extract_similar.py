# -*- coding: utf-8 -*-
from backend.models.template import Template
from backend.models.page import Article
import pandas as pd
import numpy as np
import sys

if __name__ == "__main__":

    params = sys.argv
    keys = params[1].split(",")
    Article.read_tfidf()
    print("complete reading tfidf file.")
    template = Template({"title":"test_article", "keys":keys})

    template.select_similar()
    template.recommended_infobox()
    print("Infobox: '{}'".format(template.infobox[0].title))
    template.recommended_sections()
    print("Section: {}".format(template.secs))
