#!/usr/bin/env python
# main script
# input from stdin
# args: -s -o (output options)
import sys
from lib import set_output_parser
from lib.frames.verb_frames.verb_frame_matcher import VerbFrameMatcher
from lib.frames.noun_frames.noun_frame_matcher import NounFrameMatcher
from lib.semantics.text_wrapper import TextWrapper
from lib.semantics.output.output_wrapper import OutputWrapper

# read set output file
set_output_file = sys.stdin
sentences = set_output_parser.parse(set_output_file)

# check for other cmd options
s_out = False
o_out = False
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg.strip() == '-s':
            s_out = True
        elif arg.strip() == '-o':
            o_out = True

# debug sentences
if s_out:
    for sentence in sentences:
        print str(sentence)
    print

# load frame matchers
f_v = open('frames/verb.frames.03.data', 'r')
verb_matcher = VerbFrameMatcher(f_v)
f_n = open('frames/noun.frames.02.data', 'r')
noun_matcher = NounFrameMatcher(f_n)

# create text wrapper - contains the whole text
text_wrapper = TextWrapper(sentences)

# apply frames
text_wrapper.matchSentences(verb_matcher)
text_wrapper.matchSentences(noun_matcher)

# process relations - discourse analysis
text_wrapper.processRelations()

# create output
output_wrapper = OutputWrapper(text_wrapper)
output_wrapper.createOutputObjects()
if o_out:
    output_wrapper.renderOutput()
    print
output_wrapper.renderJSON()
