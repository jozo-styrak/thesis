#!/usr/bin/env python
''' parser for valency frames analysis output '''

''' reads semantic information about frames '''
''' adapted also for more sentences '''
def parse(f):
    sentences = []
    current_sentence = []
    sentence_count = 0
    for line in f.readlines():
        if line.startswith("<s="):
            if current_sentence != [] or sentence_count > 0:
                sentences.append(current_sentence)
                current_sentence = []
            sentence_count += 1
        elif len(line) != 0:
            current_sentence.append(ValencySlot(line))
    sentences.append(current_sentence)
    return sentences
        
class ValencySlot:

    def __init__(self, line):
        self.word = line[:line.find('##')].strip()
        self.roles = line.strip()[line.find('##')+3:-1].replace(', ', ',').split(',')
        
    def getValencySlot(self):
        return self.word + ", roles: " + ', '.join(self.roles)