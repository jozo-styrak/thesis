#!/usr/bin/env python
# pipeline script for running NER

import sys

from lib.pipeline_utils import PipelineUtils
from lib.ner.ner import executeNER, changePOSTags


if len(sys.argv) > 1:
    # for development purposes on my PC
    f = open('data/desamb_out_3', 'r')
    PipelineUtils.formatDesambOutput(changePOSTags(executeNER(PipelineUtils.bufferSentences(f.readlines()))))
else:
    PipelineUtils.formatDesambOutput(changePOSTags(executeNER(PipelineUtils.bufferSentences(sys.stdin.readlines()))))
