#! /usr/bin/env python 
# Script to generate colorbrewer based colors for matplotlib
#    http://colorbrewer2.org
#
# TODO: Upgrade to https://jiffyclub.github.io/palettable/


import numpy as np
import matplotlib as mpl

import brewer2mpl


colors = brewer2mpl.get_map('Set1', 'qualitative', 7).mpl_colors

for color in colors:
    print mpl.colors.rgb2hex(color)