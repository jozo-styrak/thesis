# module containing possible forms for given slot
from lib.sentence.phrases import NPhrase, VPhrase

class Form:

    def matchPhrase(self, phrase):
        return True

# case and prepositional form
class CaseForm(Form):

    # string in form: 'preposition pronouncase', eg 'na co4', possible more values separated by '|'
    def __init__(self, form_str):
        self.form_str = form_str
        self.preposition = []
        self.case = []
        for part_str in form_str.split('|'):
            self.case.append(int(part_str[-1:]))
            if part_str.find(' ') != -1:
                self.preposition.append(part_str.split()[0])
            else:
                self.preposition.append(None)

    # matches only noun phrases based on case
    def matchPhrase(self, phrase):
        if isinstance(phrase, NPhrase):
            matches = False
            for i in range(len(self.case)):
                if self.case[i] == phrase.case:
                    if self.preposition[i] != None:
                        matches_prep = False
                        for token in phrase.tokens:
                            if self.preposition[i] == token.lemma:
                                matches_prep = True
                        if matches_prep:
                            matches = True
                    else:
                        matches = True
            return matches
        else:
            return False

    def __str__(self):
        return '{' + self.form_str + '}'

# infinitive form
class InfinitiveForm(Form):

    # matches with phrase containing verb in infinitive, tag mF
    def matchPhrase(self, phrase):
        if isinstance(phrase, VPhrase):
            matches = False
            for token in phrase.tokens:
                if 'mF' in token.tag:
                    matches = True
            return matches
        else:
            return False

    def __str__(self):
        return '{infinitive}'