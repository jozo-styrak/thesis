#!/usr/bin/env python
# main script
# run from shell script analyse_text_new
# args: set_output_file
import sys

from lib import set_parser_ver02
from lib.frames.verb_frames.verb_frame_matcher import VerbFrameMatcher
from lib.frames.noun_frames.noun_frame_matcher import NounFrameMatcher
from lib.semantics.text_wrapper import TextWrapper
from lib.semantics.output.output_wrapper import OutputWrapper

# read set output file
set_output_file = open(sys.argv[1], 'r')
sentences = set_parser_ver02.parse(set_output_file)

# debug sentences
for sentence in sentences:
    print "\n" + str(sentence)
    for clause in sentence.clauses:
        print "<clause>"
        for phrase in clause.phrases:
            print phrase
    print

# load frame matchers
f_v = open('frames/verb.frames.02.data', 'r')
verb_matcher = VerbFrameMatcher(f_v)
f_n = open('frames/noun.frames.02.data', 'r')
noun_matcher = NounFrameMatcher(f_n)

# create text wrapper
text_wrapper = TextWrapper(sentences)

# apply frames
text_wrapper.matchSentences(verb_matcher)
text_wrapper.matchSentences(noun_matcher)

# process relations
text_wrapper.processRelations()

# create output
output_wrapper = OutputWrapper(text_wrapper)
output_wrapper.createOutputObjects()
output_wrapper.renderOutput()
output_wrapper.renderJSON()