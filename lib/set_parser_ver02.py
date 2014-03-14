#!/usr/bin/env python
''' module for parsing dependency output of set utility '''
''' newer version - more object oriented'''
import re
from lib.sentence.sentence import Sentence


TAG_PATTERN = re.compile("^<(.*?)>(.*)$")
DEPENDENCY_PATTERN = re.compile("^\[([\d, ]*?)\] ->>> \[([\d, ]*?)\]$")


''' method parses set input file and creates Sentence object '''
def parse(f):
    sentences = []
    lines = f.readlines()
    # resolving of dependencies happens only when all phrases from sentence are read - because of coord phrase
    dependencies = {}
    i = 0
    while i < len(lines):
        newLine = OutputLine(lines[i])
        # beggining of a new sentence - reads tokens, lemmas and tags
        if newLine.isTag and newLine.tag == 's':
            sentences.append(Sentence(newLine.value, OutputLine(lines[i+1]).value, OutputLine(lines[i+2]).value))
            i += 2
        # new clause - skips token values, reads num and conjunction
        elif newLine.isTag and newLine.tag == 'clause':
            line2 = OutputLine(lines[i+2])
            sentences[len(sentences)-1].addNewClause(OutputLine(lines[i+1]).value, line2.value[line2.value.find('):')+3:])
            i += 2
        # new verb phrase - skips token values and lemmas, reads num and head
        elif newLine.isTag and newLine.tag == 'vp':
            line2 = OutputLine(lines[i+2])
            line3 = OutputLine(lines[i+3])
            sentences[len(sentences)-1].addNewVerbPhrase(newLine.value[newLine.value.find('):')+3:], line2.value[line2.value.find('):')+3:], line3.value)
            i += 3
        # new noun phrase or coordination phrase - skips token values and lemmas, reads num, head and dependency line
        elif newLine.isTag and (newLine.tag == 'phr' or newLine.tag == 'coord' or newLine.tag == 'inter'):
            line1 = OutputLine(lines[i+1])
            line2 = OutputLine(lines[i+2])
            line3 = OutputLine(lines[i+3])
            line4 = OutputLine(lines[i+4])
            # checks whether next line contains dependency
            dependency = line4.dependentOn if not line4.isTag else None
            # if line isTag / does not contain dependency / moves one down in file
            i_shift = 4 if not line4.isTag else 3
            # add identificator for dependency relation for latter processing
            if dependency != None:
                dependencies[line2.value[line2.value.find('):')+3:]] = dependency
            sentences[len(sentences)-1].addNewNounPhrase(newLine.value[newLine.value.find('):')+3:], line1.value, line2.value[line2.value.find('):')+3:], line3.value)
            i += i_shift
        # end of sentence, resolve dependencies
        elif newLine.isTag and newLine.tag == '/s':
            for num in dependencies.keys():
                dependent_phrase = sentences[len(sentences)-1].getPhraseByNum(num)
                parent_phrase = sentences[len(sentences)-1].getPhraseByNum(dependencies[num])
                if dependent_phrase != None and parent_phrase != None:
                    dependent_phrase.dependent_on = parent_phrase
            dependencies = {}
            i += 1
        else:
            i += 1
    return sentences


''' applies patterns to the input line '''
''' if it is standard line, returns token information '''
''' if it is line with dependency ([1] ->>> [2]) returns this information '''
def getTagAndData(line):
    if TAG_PATTERN.match(line):
        return TAG_PATTERN.search(line).groups()
    elif DEPENDENCY_PATTERN.match(line):
        return DEPENDENCY_PATTERN.search(line).groups()[1].replace(',', '').strip()
    else:
        return False
     
        
''' class representing one line from set output '''
class OutputLine:
    
    def __init__(self, line):
        token = getTagAndData(line)
        if type(token) is tuple:
            self.isTag = True
            self.tag = token[0].strip()
            self.value = token[1].strip()
        else:
            self.isTag = False
            self.dependentOn = token