#!/usr/bin/env python

import sys

from web_extraction import utils


''' arguments: http link, cca count:), directory '''
utils.createTextCorpora(sys.argv[1].strip(), int(sys.argv[2]), sys.argv[3].strip())
