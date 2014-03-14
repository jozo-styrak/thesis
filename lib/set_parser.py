#!/usr/bin/env python
''' module for parsing dependency output of set utility '''
import re

TAG_PATTERN = re.compile("^<(.*?)>(.*)$")
DEPENDENCY_PATTERN = re.compile("^\[([\d, ]*?)\] ->>> \[([\d, ]*?)\]$")

def parse(file):
    sentences = []
    lines = file.readlines()
    i = 0
    while i < len(lines):
        newLine = OutputLine(lines[i])
        if newLine.isTag and newLine.tag=='s':
            sentences.append(Sentence(newLine.value, OutputLine(lines[i+1]).value, OutputLine(lines[i+2]).value))
            i += 2
        if newLine.isTag and newLine.tag=='clause':
            sentences[len(sentences)-1].clauses.append(Clause(newLine.value, OutputLine(lines[i+1]).value, OutputLine(lines[i+2]).value))
            i += 2
        if newLine.isTag and newLine.tag=='vp':
            sentences[len(sentences)-1].clauses[len(sentences[len(sentences)-1].clauses)-1].phrases.append(VPhrase(newLine.value, OutputLine(lines[i+1]).value, OutputLine(lines[i+2]).value, OutputLine(lines[i+3]).value))
            i += 3
        if newLine.isTag and newLine.tag=='phr':
            dependency = None
            i_shift = 3
            if not OutputLine(lines[i+4]).isTag:
                dependency = OutputLine(lines[i+4]) 
                i_shift = 4
            sentences[len(sentences)-1].clauses[len(sentences[len(sentences)-1].clauses)-1].phrases.append(NPhrase(newLine.value, OutputLine(lines[i+1]).value, OutputLine(lines[i+2]).value, OutputLine(lines[i+3]).value, sentences[len(sentences)-1].clauses[len(sentences[len(sentences)-1].clauses)-1].phrases, dependency))
            i += i_shift
        else:
            i += 1
    return sentences
        
def getTagAndData(line):
    if TAG_PATTERN.match(line):
        return TAG_PATTERN.search(line).groups()
    elif DEPENDENCY_PATTERN.match(line):
        return DEPENDENCY_PATTERN.search(line).groups()[1].replace(',', '').strip()
    else:
        return False
        
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

class Sentence:

    def __init__(self, s, lemmas, tags):
        self.s = s
        self.lemma = lemmas
        self.tag = tags
        self.clauses = []

class Clause:

    def __init__(self, clause, num, conj):
        self.clause = clause
        self.num = num
        self.conj = conj
        self.phrases = []

class SetPhrase:

    def __init__(self, phr, lemma, num, head):
        self.phr = phr[phr.find('):')+3:]
        self.lemma =  lemma[lemma.find('):')+3:]
        self.num =  num[num.find('):')+3:]
        self.head = head
        
    def toString(self):
        return self.lemma + ' (' + self.num + ')'

class VPhrase(SetPhrase):

    def __init__(self, vp, lemma, num, head):
        SetPhrase.__init__(self, vp, lemma, num, head)
        
class NPhrase(SetPhrase):

     def __init__(self, phr, lemma, num, head, phrases, dependency):
        SetPhrase.__init__(self, phr, lemma, num, head)
        if dependency == None:
            self.dependentOn = None
        else:
            for phrase in phrases:
                if phrase.num == dependency.dependentOn:
                    self.dependentOn = phrase