#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''  syntactic preprocessor '''
'''  connects abbreviations and number values '''
'''  connect recommendations into prep. phrases '''
import sys
import re

REAL_NUMBER_PATTERN = re.compile("[\+-]*\d+[\.,/:]*\d*")
NUM_FOLLOW = ['KČ', 'Kč', '%', 'euro', 'USD', 'mil', 'tis', 'PLN', 'NOK', 'HUN', 'GBP', 'AUD', 'JPY', 'CHF', 'RUB', 'eur', 'dolar']
RECOMMENDATIONS = ['držet', 'koupit', 'kupovat', 'redukovat', 'akumulovat', 'prodat', 'buy', 'hold', 'sell', 'neutral', 'perform', 'underperform', 'underweight', 'accumulate', 'outperform', 'swap', 'overweight', 'reduce', 'equalweight']


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

def connectTokens(buffered_sentences):
    new_sentences = []
    for sentence in buffered_sentences:
        new_sentence = []
        new_sentence.append(sentence[0])
        i = 1
        while i < len(sentence):
            # connect abbreviations - in a new version also connects numbers with abbreviations
            if (sentence[i][2] == 'kA' or sentence[i][2] == 'kIx)' or sentence[i][2] == 'kIx(') and (new_sentence[len(new_sentence)-1][2] == 'kA' or new_sentence[len(new_sentence)-1][2].find('k1') != -1):
                new_sentence[len(new_sentence)-1][0] += '' + sentence[i][0]
                new_sentence[len(new_sentence)-1][1] += '' + sentence[i][1]
            # connect numbers with some follow strings
            #elif new_sentence[len(new_sentence)-1][2].find('k4') != -1 and sentence[i][1] in NUM_FOLLOW:
            elif REAL_NUMBER_PATTERN.match(new_sentence[len(new_sentence)-1][0]) and sentence[i][1] in NUM_FOLLOW:
                new_sentence[len(new_sentence)-1][0] += '' + sentence[i][0]
                new_sentence[len(new_sentence)-1][1] += '' + sentence[i][1]
            # connect preposition and number
            elif new_sentence[len(new_sentence)-1][2].find('k7') != -1 and sentence[i][2].find('k4') != -1:
                #new_sentence[len(new_sentence)-1][0] += '_' + sentence[i][0]
                #new_sentence[len(new_sentence)-1][2] += '_' + sentence[i][2]
                new_element = []
                new_element.append(sentence[i][0])
                new_element.append(sentence[i][1])
                new_element.append('k1nPgIc' + new_sentence[len(new_sentence)-1][2][new_sentence[len(new_sentence)-1][2].find('c')+1])
                new_sentence.append(new_element)
            # changes the case of following recommendation to match preposition case / added, change of case if word 'doporuceni' preceeds
            elif sentence[i][1] in RECOMMENDATIONS and ((new_sentence[len(new_sentence)-1][2] == 'kIx\"' and (new_sentence[len(new_sentence)-2][2].startswith('k7') or new_sentence[len(new_sentence)-2][1] == 'doporučení')) or new_sentence[len(new_sentence)-1][2].startswith('k7') or new_sentence[len(new_sentence)-1][1] == 'doporučení'):
                if new_sentence[len(new_sentence)-1][2].startswith('k7') or new_sentence[len(new_sentence)-1][1] == 'doporučení':
                    new_element = []
                    new_element.append(sentence[i][0])
                    new_element.append(sentence[i][1])
                    new_element.append('k2nPgIc' + new_sentence[len(new_sentence)-1][2][new_sentence[len(new_sentence)-1][2].find('c')+1])
                    new_sentence.append(new_element)
                else:
                    new_element = []
                    new_element.append(sentence[i][0])
                    new_element.append(sentence[i][1])
                    new_element.append('k2nPgIc' + new_sentence[len(new_sentence)-2][2][new_sentence[len(new_sentence)-2][2].find('c')+1])
                    new_sentence.pop()
                    new_sentence.append(new_element)
                    if sentence[i+1][2] == 'kIx\"':
                        i += 1                    
            else:
                new_sentence.append(sentence[i])
            i += 1
        new_sentences.append(new_sentence)
    return new_sentences
    
def formatDesambOutput(sentences):
    i = 1
    for sentence in sentences:
        print '<s desamb=\"',i,'\">'
        for word in sentence:
            print '\t'.join(word)
        print "</s>"
        i += 1
        
if len(sys.argv) > 1:
    f = open('data/desamb_out_3', 'r')
    formatDesambOutput(connectTokens(bufferSentences(f.readlines())))
else:
    formatDesambOutput(connectTokens(bufferSentences(sys.stdin.readlines())))