# -*- coding: utf-8 -*-

from lib.frames.constraints_checker import ConstraintsChecker

# does role need to have information about the referencing phrase/token??

# class representing semantic role which translates to verbalex roles
class SemanticRole:

    def __init__(self, first_lvl_role, second_lvl_role):
        self.first_level_role = first_lvl_role
        self.second_level_role = second_lvl_role
        # referring phrase
        self.phrase = None
        # containing relation
        self.relation = None
        # corefering phrase
        self.coreferent = None
        # if the role is invalid for given phrase, done in constraints check
        self.invalid = False

    # return containing relation
    def getRelation(self):
        return self.relation

    # set refering phrase (and coreferent)
    def setPhrase(self, phrase):
        self.phrase = phrase
        self.coreferent = self.phrase

    # check whether this role's phrase has kA as subpart
    def filledWithNE(self):
        # filled = False
        # if self.phrase != None:
        #     for token in self.phrase.tokens:
        #         if token.value.endswith('kA'):
        #             filled = True
        #         # elif token.lemma in ['banka', 'společnost']:
        #         #     filled = True
        # return filled
        return ConstraintsChecker.isNamedEntity(self.phrase) if self.phrase != None else False

    def __str__(self):
        ret = 'Phrase \'' + str(self.phrase) + '\': ' if self.phrase != None else 'Ellipsed : '
        invalid_note = '' if not self.invalid else ' [invalid role]'
        return ret + '{ ' + self.second_level_role + ' as ' + self.first_level_role + ' }' + invalid_note