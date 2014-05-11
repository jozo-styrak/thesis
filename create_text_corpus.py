#!/usr/bin/env python
# downloads web page contents to given directory
import sys

from lib.web_extraction import web_utils


# arguments: http link, cca count:), directory
web_utils.createTextCorpora(sys.argv[1].strip(), int(sys.argv[2]), sys.argv[3].strip())
