# -*- coding: utf-8 -*-
from backend.templa.templa import Templa
import pandas as pd
import numpy as np
import sys

if __name__ == "__main__":

    params = sys.argv
    keys = params[1].split(",")
    templa = Templa()

    similars = templa.select_similar(keys)
    for a in similars:
        print("title: {} => infobox: {}".format(a.title, a.infobox))
        print("keys = {}".format(a.keywords))
