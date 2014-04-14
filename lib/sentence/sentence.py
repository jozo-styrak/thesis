from lib.sentence.phrases import NPhrase, VPhrase, Clause


class Token:
    def __init__(self, value, lemma, tag):
        self.value = value
        self.lemma = lemma
        self.tag = tag
        self.semantic_roles = []

    def __str__(self):
        # return self.value + ' (' + ', '.join(self.semantic_roles) + ')' if self.semantic_roles != [] else self.value
        return self.value


class Sentence:
    def __init__(self, value, lemma, tag):
        self.tokens = []
        self.clauses = []
        self.relevant_sentence = False
        values = value.split()
        lemmas = lemma.split()
        tags = tag.split()
        for i in range(len(values)):
            self.tokens.append(Token(values[i], lemmas[i], tags[i]))

    def getTokenByValue(self, value):
        ret_token = None
        for token in self.tokens:
            if token.value == value:
                ret_token = token
        return ret_token

    def getPhraseTokens(self, phrase):
        ret_tokens = []
        for token in phrase.split():
            ret_tokens.append(self.getTokenByValue(token))
        return ret_tokens

    def getPhraseByNum(self, num):
        ret_phrase = None
        for clause in self.clauses:
            for phrase in clause.phrases:
                if phrase.num == num:
                    ret_phrase = phrase
        return ret_phrase

    def getTokenByNum(self, num):
        return self.tokens[int(num)-1]

    def addNewClause(self, num, conj):
        self.clauses.append(Clause(num, self.getTokenByValue(conj)))

    def addNewVerbPhrase(self, phrase_value, num, head):
        for clause in self.clauses:
            if clause.inClause(num):
                phrase_tokens = self.getPhraseTokens(phrase_value)
                #vp = VPhrase(num, phrase_tokens[num.split().index(head)])
                vp = VPhrase(num, self.getTokenByNum(head))
                vp.tokens = phrase_tokens
                clause.phrases.append(vp)

    def addNewNounPhrase(self, phrase_value, tag, num, head, is_coord):
        for clause in self.clauses:
            if clause.inClause(num):
                phrase_tokens = self.getPhraseTokens(phrase_value)
                #np = NPhrase(tag, num, phrase_tokens[num.split().index(head)])
                np = NPhrase(tag, num, self.getTokenByNum(head), is_coord)
                np.tokens = phrase_tokens
                clause.phrases.append(np)

    # return phrases which are dependent on specified phrase
    def getDependentPhrases(self, phrase):
        dependent = []
        for clause in self.clauses:
            for phr in clause.phrases:
                if isinstance(phr, NPhrase) and phrase is phr.dependent_on:
                    dependent.append(phr)
        return dependent

    # return token that follows given phrase
    def getFollowingToken(self, phrase):
        following_num = phrase.num.split()[-1:]
        token = None
        for clause in self.clauses:
            for phr in clause.phrases:
                if following_num in phr.num.split():
                    token = phr.getTokenByNum(following_num)
        return token

    def __str__(self):
        values = []
        for token in self.tokens:
            values.append(str(token))
        return ' '.join(values)

    # ''' adds semantic information to sentence + checks if is relevant '''
    # def addSemanticRoles(self, valency_slots):
    #     if len(valency_slots) > 0:
    #         self.relevant_sentence = True
    #         for valency_slot in valency_slots:
    #             token = self.getTokenByValue(valency_slot.word)
    #             if token != None:
    #                 token.semantic_roles = valency_slot.roles
    #
    # ''' redirects recommendation information dependency to point to the verb '''
    # ''' currently unused '''
    # def redirectRecommendationDependancy(self):
    #     for clause in self.clauses:
    #         for phrase in clause.phrases:
    #             if isinstance(phrase, NPhrase) and phrase.tokens[0].tag.startswith('k7') and phrase.tokens[0].value.find('_') != -1:
    #                 phrase.dependentOn = clause.getVPhrase()
    #
    # def containsLemma(self, lemma):
    #     ret = False
    #     for clause in self.clauses:
    #         for phrase in clause.phrases:
    #             for token in phrase.tokens:
    #                 if lemma == token.lemma:
    #                     ret = True
    #     return ret
    #
    # def containsLemmaSubstring(self, lemma):
    #     ret = False
    #     for clause in self.clauses:
    #         for phrase in clause.phrases:
    #             for token in phrase.tokens:
    #                 if token.lemma.find(lemma) != -1:
    #                     ret = True
    #     return ret