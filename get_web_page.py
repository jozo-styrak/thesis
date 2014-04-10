#!/usr/bin/env python
# takes one argument - url of web page
from urllib import urlopen
import sys

from lib.web_extraction import web_utils


web_utils.getTextPage(web_utils.readArticle(urlopen(sys.argv[1]).read(), sys.argv[1]), sys.stdout)
