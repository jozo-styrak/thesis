from lib.semantics.utils.utils import Utils
from lib.semantics.utils.role_resolver import RoleResolver

# grouping object for all the relations and roles in the text
# for now also doing coreference, ellipse and named entity resolution
class TextWrapper:

    def __init__(self, sentences):
        self.relations = []
        self.sentences = sentences
        # self.fetchRelations()

    # collects relations into relation list from given sentences
    def fetchRelations(self):
        for sentence in self.sentences:
            for clause in sentence.clauses:
                if clause.containing_relation != None:
                    self.relations.append(clause.containing_relation)

    # match sentences with given frame matcher object
    def matchSentences(self, frame_matcher):
        for sentence in self.sentences:
            frame_matcher.matchFrames(sentence)


    # preprocess relation
    # resolve roles, apply constraints, resolve coreferents,...
    def processRelations(self):

        # create relations list
        self.fetchRelations()

        # resolve <actor> roles
        RoleResolver.resolveActorRoles(self.relations, self.sentences)

        # apply constraints and remove invalid roles
        self.applyConstraints()

        # debug
        print '\n---------------------------------------------------'
        self.printRelations()
        print '---------------------------------------------------'

        # look over all relations
        for relation in self.relations:

            # check whether relation contains state/price information
            # what's the point?
            if relation.containsMainInformation():

                # first find agency
                # agency_role = relation.getSecondLevelRole('<actor_agency:1>')
                agency_roles = relation.getSecondLevelRoles('<actor_agency:1>')
                for agency_role in agency_roles:
                    self.findNamedEntityCoreferent(agency_role)

                    # ...then resolve stock role
                stock_roles = relation.getSecondLevelRoles('<actor_stock:1>')
                for stock_role in stock_roles:
                    self.findNamedEntityCoreferent(stock_role)

    # resolve actor roles
    # currently just make them agencies
    def setActorRoles(self):
        for relation in self.relations:
            for role in relation.roles:
                if role.second_level_role == '<actor:1>':
                    role.second_level_role = '<actor_agency:1>'


    # apply constraints to all identified roles and delete invalid roles
    def applyConstraints(self):
        for sentence in self.sentences:
            Utils.applyConstraints(sentence)
        for relation in self.relations:
            for role in relation.roles:
                if role.invalid:
                    relation.roles.remove(role)

    # new coreference resolution method
    # slightly changed algorithm & returns just one item
    def getCoreferent(self, role):
        coreferent_phrase = None

        # sequentially add clauses to the list order
        clauses = []
        clause_found = False
        for sentence in self.sentences:
            for clause in sentence.clauses:
                # found containing clause
                if clause == role.getRelation().containing_clause:
                    clause_found = True
                    # if clause was just found and the antecedent is not a pronoun, search also current clause
                    if role.phrase == None or  (role.phrase != None and not 'k3yR' in role.phrase.tokens[0].tag):
                        clauses.insert(0, clause)
                # clause wasn't found yet, add clause at the beginning
                elif not clause_found:
                    clauses.insert(0, clause)
                # clause was found, add clause at the end
                else:
                    clauses.append(clause)

        # find coreferent
        i = 0
        while i < len(clauses) and coreferent_phrase == None:
            j = 0
            while j < len(clauses[i].phrases) and coreferent_phrase == None:
                phrase_role = clauses[i].phrases[j].hasRole(role.second_level_role)
                # newer version - search also base roles
                if not phrase_role:
                    phrase_role = clauses[i].phrases[j].hasBaseRole(role.second_level_role)
                if phrase_role and phrase_role.filledWithNE():
                    coreferent_phrase = clauses[i].phrases[j]
                j += 1
            i += 1

        return coreferent_phrase


    # wrapping method for resolution
    def findNamedEntityCoreferent(self, role):
        if role != None:
            if not role.filledWithNE():
                # new version, returns just one
                role.coreferent = self.getCoreferent(role)

    # debug method
    def printRelations(self):
        for relation in self.relations:
            print relation

    # debug method
    def printActors(self):
        print '---------------------------- ACTOR ROLES ---------------------------------'
        for relation in self.relations:
            for role in relation.roles:
                if role.second_level_role.startswith('<actor') and role.filledWithNE():
                    print role
