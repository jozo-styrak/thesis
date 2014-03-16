#!/usr/bin/env python

from urllib import urlopen
import sys

from web_extraction import utils


utils.getTextPage(utils.readArticle(urlopen(sys.argv[1]).read(), sys.argv[1]), sys.stdout)
