from lib.frames.constraints_checker import ConstraintsChecker

# grouping object for all the relations and roles in the text
# for now also doing coreference, ellipse and named entity resolution
class TextInformation:

    def __init__(self, relations, sentences):
        self.relations = relations
        self.sentences = sentences

    # wrapping output method
    def getTextInformation(self):

        # debug
        # self.printRelations()

        # resolve <actor> roles
        self.resolveActorRoles()

        # join relations within the same clause
        self.preprocessRelations()


        # apply constraints
        constraints_checker = ConstraintsChecker()
        for sentence in self.sentences:
            constraints_checker.applyConstraints(sentence)

        # debug
        self.printRelations()

        # for now it returns just arrays with filtered phrases
        ret_objects = []

        # look over all relations
        for relation in self.relations:

            # check whether relation contains state/price information
            if relation.containsMainInformation():

                # check whether agens or patient is omitted
                if not relation.filledWithNE('<actor_agency:1>') or not relation.filledWithNE('<actor_stock:1>'):

                    # first find agency
                    agency_role = relation.getSecondLevelRole('<actor_agency:1>')
                    if agency_role != None:
                        if not relation.filledWithNE('<actor_agency:1>'):
                            candidates = self.getCandidateCoreferents(agency_role)
                            # print "\ncandidate phrases for " + str(agency_role)
                            # for phrase in candidates:
                            #     print phrase
                            # just take the first one here
                            if len(candidates) > 0:
                                agency_role.coreferent = candidates[0]

                    # ...then resolve stock role
                    stock_role = relation.getSecondLevelRole('<actor_stock:1>')
                    if stock_role != None:
                        if not relation.filledWithNE('<actor_stock:1>'):
                            candidates = self.getCandidateCoreferents(stock_role)
                            # print "\ncandidate phrases for " + str(stock_role)
                            # for phrase in candidates:
                            #     print phrase
                            # just take the first one here
                            if len(candidates) > 0:
                                stock_role.coreferent = candidates[0]

                # fill object with values from relation
                ret_objects.append(relation.getInformationObject())

        return ret_objects

    # preprocessing method
    # join relations within the same sentence clause
    # basicaly compressing relations
    def preprocessRelations(self):
        new_relations = []
        for sentence in self.sentences:
            for clause in sentence.clauses:
                clause_relations = clause.getSemanticRelations()
                if len(clause_relations) == 1:
                    clause_relations[0].containing_clause = clause
                    new_relations.append(clause_relations[0])
                elif len(clause_relations) > 1:
                    # take roles from relations and stack them to relation created as first
                    for i in range(1,len(clause_relations)):
                        for role in clause_relations[i].roles:
                            if clause_relations[0].getSecondLevelRole(role.second_level_role) == None:
                                clause_relations[0].addNewRole(role)
                        clause_relations[i] = None
                    clause_relations[0].containing_clause = clause
                    new_relations.append(clause_relations[0])
        # new relations
        self.relations = new_relations

    # resolve actor roles
    # currently just make them agencies
    def resolveActorRoles(self):
        for relation in self.relations:
            for role in relation.roles:
                if role.second_level_role == '<actor:1>':
                    role.second_level_role = '<actor_agency:1>'

    # returns candidate coreferents for given role type from text
    # return type: Phrase
    def getCandidateCoreferents(self, role):
        candidates = []

        # split sentences among previous, current and next
        previous = []
        current = None
        next = []
        clause_found = False
        for sentence in self.sentences:
            found_now = False  # help variable
            for clause in sentence.clauses:
                # found containing clause
                if clause == role.getRelation().containing_clause:
                    clause_found = True
                    found_now = True
            if found_now:
                current = sentence
            elif not clause_found:
                previous.append(sentence)
            else:
                next.append(sentence)

        # create order of sentences
        sentence_order = []
        sentence_order.append(current)
        # previous sentences in reversed order
        for sentence in previous[::-1]:
            sentence_order.append(sentence)
        # next sentences in normal order
        for sentence in next:
            sentence_order.append(sentence)


        # get possible candidates from given order
        for sentence in sentence_order:
            for clause in sentence.clauses:
                for phrase in clause.phrases:
                    phrase_role = phrase.hasRole(role.second_level_role)
                    if phrase_role and phrase_role.filledWithNE():
                        candidates.append(phrase)

        return candidates

    # debug method
    def printRelations(self):
        for relation in self.relations:
            print relation


