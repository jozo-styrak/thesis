#!/usr/bin/env python
from lib import set_parser_ver02
from lib.frames.frame_matcher import FrameMatcher
import sys


set_output_file = open(sys.argv[1], 'r')
sentences = set_parser_ver02.parse(set_output_file)

f = open('data/patterns.data', 'r')
frame_matcher = FrameMatcher(f)
# frame_matcher.printFrames()

all = 0
incorrect = 0
for sentence in sentences:
    if not frame_matcher.matchFrames(sentence):
        print '\n' + str(sentence)
        for clause in sentence.clauses:
            print "<clause>"
            for phrase in clause.phrases:
                print phrase
        print
        incorrect += 1
    all += 1

print str(incorrect) + '/' + str(all)