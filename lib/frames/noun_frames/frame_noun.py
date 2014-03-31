from lib.sentence.phrases import NPhrase
from lib.semantics.semantic_relation import SemanticRelation
from lib.semantics.semantic_role import SemanticRole
import re


# pattern to identify real numbers
REAL_NUMBER_PATTERN = re.compile('[\+-]*\d+[\.,/:]*\d*')

# abstract class for all types of noun phrase types
class FrameNoun:

    def __init__(self):
        self.complements = []
        self.role = None

    # create list of phrases from dependency tree based on given phrase
    def generateDependencyTree(self, clause, phrase):
        changed = True
        tree_phrases = clause.getDependentPhrases(phrase)
        while changed:
            changed = False
            for phr in tree_phrases:
                dependent = clause.getDependentPhrases(phr)
                for dep_phr in dependent:
                    if not dep_phr in tree_phrases:
                        changed = True
                        tree_phrases.append(dep_phr)
        return tree_phrases


    # return candidate phrases for complements for given phrase for containing clause
    def getCandidatePhrases(self, clause, phrase):
        phrases = self.generateDependencyTree(clause, phrase)
        # for phr in clause.getSucceedingPhrases(phrase):
        #     if isinstance(phr, NPhrase) and phr.dependent_on == None and phr not in phrases:
        #         phrases.append(phr)
        return phrases

    # unmatch all complements after usage
    def resetFrame(self):
        for complement in self.complements:
            complement.matched = False

    # whole matching method
    def matchClauseTokens(self, clause):
        relations = []
        for phrase in clause.phrases:

            # does any frame noun match some phrase in clause?
            # takes coordination phrases as one
            if isinstance(phrase, NPhrase) and not phrase.isInCoordination() and self.matchesPhrase(phrase) and not phrase.roleConflict(self.role):
                relation = None
                roles = []

                # for now, if phrase is already in a relation, use this relation
                if len(phrase.semantic_roles) > 0:
                    relation = phrase.semantic_roles[0].getRelation()  # use first, but they're all the same

                # add semantic role to matching phrase
                # if role does not exist, create new one
                # if exists, use this one
                # and at same time tries to upgrade existing base role to specific role
                if not phrase.hasRole(self.role):
                    role = SemanticRole('OBJ', self.role)
                    role.phrase = phrase
                    phrase.addSemanticRole(role)
                    roles.append(role)
                else:
                    # use this relation
                    relation = phrase.hasRole(self.role).getRelation()

                # match complements
                for phr in self.getCandidatePhrases(clause, phrase):
                    for complement in self.complements:
                        if not complement.matched:
                            # does complement match?
                            if complement.matchPhrase(phr):
                                # does given phrase already have given role?
                                if not phr.hasRole(complement.role):
                                    role = SemanticRole('COMPL', complement.role)
                                    role.phrase = phr
                                    phr.addSemanticRole(role)
                                    roles.append(role)
                                elif phr.hasRole(complement.role) and relation == None:  # if given phrase already has given role, use this relation
                                    relation = phr.hasRole(complement.role).getRelation()

                # if there was no relation detected, create new one
                if relation == None:
                    relation = SemanticRelation()

                # add roles to relation
                for r in roles:
                    r.relation = relation
                    relation.addNewRole(r)

                relations.append(relation)
        return relations

    # abstract method
    def matchesPhrase(self, phrase):
        return False


# general type of phrase - matching of given lemma
class GeneralPhrase(FrameNoun):

    def __init__(self, noun_str):
        FrameNoun.__init__(self);
        self.nouns = []
        for noun in noun_str.split(';'):
            self.nouns.append(noun.strip())

    # whether the phrase contains one of frame nouns
    def matchesPhrase(self, phrase):
        contains = False
        for token in phrase.tokens:
            if token.lemma in self.nouns:
                contains = True
        return contains

    def __str__(self):
        ret_str = 'nouns: ' + ','.join(self.nouns) + '\nrole: ' + str(self.role) + '\ncomplements: '
        for complement in self.complements:
            ret_str += str(complement) + ' '
        return ret_str.strip()


# class for named entities in text
class NamedEntity(FrameNoun):

    def __init__(self):
        FrameNoun.__init__(self)

    def matchesPhrase(self, phrase):
        contains = False
        for token in phrase.tokens:
            if token.value.endswith('_kA'):
                contains = True
        return contains


# class for numbers with number follow - price, percentage,...
class NumberEntity(FrameNoun):

    def __init__(self):
        FrameNoun.__init__(self)

    def matchesPhrase(self, phrase):
        contains = False
        for token in phrase.tokens:
            if REAL_NUMBER_PATTERN.match(token.value.split('_')[0]):
                contains = True
        return contains
