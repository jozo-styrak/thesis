from lib.sentence.phrases import NPhrase
from lib.semantics.semantic_relation import SemanticRelation
from lib.semantics.semantic_role import SemanticRole

# abstract class for all types of noun phrase types
class FrameNoun:

    # abstract method
    # frame tries to find one of frame nouns/identifier in given clause and then tries to match given complements
    def  matchClauseTokens(self, clause):
        pass

# general type of phrase - matching of given lemma
class GeneralPhrase(FrameNoun):

    def __init__(self, noun_str):
        self.nouns = []
        for noun in noun_str.split(';'):
            self.nouns.append(noun.strip())
        self.complements = []
        self.role = None

    # whether the phrase contains one of frame nouns
    def containsFrameNoun(self, phrase):
        contains = False
        for token in phrase.tokens:
            if token.lemma in self.nouns:
                contains = True
        return contains

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
        for phr in clause.getSucceedingPhrases(phrase):
            if phr not in phrases:
                phrases.append(phr)
        return phrases

    def matchClauseTokens(self, clause):
        relations = []
        for phrase in clause.phrases:

            # does any frame noun match some phrase in clause?
            if isinstance(phrase, NPhrase) and self.containsFrameNoun(phrase):

                # does for matched phrase already exist relation?
                relation = SemanticRelation() if len(phrase.semantic_roles) == 0 else phrase.semantic_roles[0].getRelation()

                # if phrase doesn't have one, add new semantic role
                if len(phrase.semantic_roles) == 0:
                    sec_lvl_role = self.role if self.role != None else '<unknown>'
                    role = SemanticRole('OBJ', sec_lvl_role, relation)
                    role.phrase = phrase
                    phrase.addSemanticRole(role)
                    relation.roles.append(role)

                # match complements
                for phr in self.getCandidatePhrases(clause, phrase):
                    for complement in self.complements:
                        if not complement.matched:
                            if complement.matchPhrase(phr):
                                if len(phr.semantic_roles) == 0:
                                    role = SemanticRole('COMPL', complement.role, relation)
                                    role.phrase = phr
                                    phr.addSemanticRole(role)
                                    relation.roles.append(role)
                relations.append(relation)
        return relations

    def resetFrame(self):
        for complement in self.complements:
            complement.matched = False

    def __str__(self):
        ret_str = 'nouns: ' + ','.join(self.nouns) + '\nrole: ' + str(self.role) + '\ncomplements: '
        for complement in self.complements:
            ret_str += str(complement) + ' '
        return ret_str.strip()