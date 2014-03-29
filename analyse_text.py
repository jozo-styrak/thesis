#!/usr/bin/env python
''' text analysator - creates syntactic structure from set ouput with a bit of semantic information from valency frames '''
''' args: set output file, get-valency-frames output file '''
import sys

from lib import set_parser_ver02
from lib.frames.verb_frames.verb_frame_matcher import VerbFrameMatcher
from lib.frames.noun_frames.noun_frame_matcher import NounFrameMatcher


set_output_file = open(sys.argv[1], 'r')
sentences = set_parser_ver02.parse(set_output_file)

for sentence in sentences:
    print "\n" + str(sentence)
    for clause in sentence.clauses:
        print "<clause>"
        for phrase in clause.phrases:
            print phrase
    print

f_v = open('frames/verb.frames.data', 'r')
verb_matcher = VerbFrameMatcher(f_v)

f_n = open('frames/noun.frames.data', 'r')
noun_matcher = NounFrameMatcher(f_n)

print '************************* MATCHING FRAMES *************************************************'

all = 0
correct = 0
for sentence in sentences:
    relations = verb_matcher.matchFrames(sentence)
    noun_relations = noun_matcher.matchFrames(sentence)
    for noun_relation in noun_relations:
        if not noun_relation in relations:
            relations.append(noun_relation)
    if relations:
        print sentence
        for relation in relations:
            print relation
        correct += 1
    all += 1


print str(correct) + '/' + str(all)