#!/usr/bin/env python
import sys

from lib.POS_editor import editTags


# from list of sentences buffer lines for each sentence
def bufferSentences(lines):
    sentences = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('<s'):
            sentence = []
            i += 1
            while not lines[i].startswith('</s>'):
                sentence.append(lines[i].strip().split())
                i += 1
            sentences.append(sentence)
        i += 1
    return sentences

# format output into desamb type format
def formatDesambOutput(sentences):
    i = 1
    for sentence in sentences:
        print '<s desamb=\"',i,'\">'
        for word in sentence:
            print '\t'.join(word)
        print "</s>"
        i += 1

if len(sys.argv) > 1:
    f = open('data/desamb_out_2', 'r')
    formatDesambOutput(editTags(bufferSentences(f.readlines())))
else:
    formatDesambOutput(editTags(bufferSentences(sys.stdin.readlines())))