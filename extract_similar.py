# -*- coding: utf-8 -*-
from backend.models.template import Template
import pandas as pd
import numpy as np
import sys

if __name__ == "__main__":

    params = sys.argv
    keys = params[1].split(",")
    template = Template({"title":"test_article", "keys":keys})

    template.select_similar()
    template.reccomended_infobox()
