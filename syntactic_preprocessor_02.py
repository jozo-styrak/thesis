#!/usr/bin/env python
import sys

from lib.POS_editor import editTags
from lib.pipeline_utils import PipelineUtils

if len(sys.argv) > 1:
    f = open('data/desamb_out_2', 'r')
    PipelineUtils.formatDesambOutput(editTags(PipelineUtils.bufferSentences(f.readlines())))
else:
    PipelineUtils.formatDesambOutput(editTags(PipelineUtils.bufferSentences(sys.stdin.readlines())))