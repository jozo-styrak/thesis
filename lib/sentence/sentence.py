from lib.sentence.phrases import NPhrase, VPhrase, Clause

# class representing one word token - one line from desamb output with added semantic roles
class Token:
    def __init__(self, value, lemma, tag):
        self.value = value
        self.lemma = lemma
        self.tag = tag
        self.semantic_roles = []

    def __str__(self):
        # return self.value + ' (' + ', '.join(self.semantic_roles) + ')' if self.semantic_roles != [] else self.value
        return self.value

# class representing whole sentence structure
# created from set output
# contains list of clause objects, which contain phrases
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

    # return list of tokens of given phrase
    def getPhraseTokens(self, phrase):
        ret_tokens = []
        for token in phrase.split():
            ret_tokens.append(self.getTokenByValue(token))
        return ret_tokens

    # based on num identification in set output
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
    def getFollowingTokenToPhrase(self, phrase):
        following_num = int(phrase.num.split()[-1:][0])
        token = None if following_num == len(self.tokens) else self.tokens[following_num]
        return token

    # return token that follows given phrase
    def getFollowingTokenToToken(self, token):
        next_token = None
        for i in range(len(self.tokens)):
            if self.tokens[i] == token and i < len(self.tokens):
                next_token = self.tokens[i+1]
        return next_token

    def __str__(self):
        values = []
        for token in self.tokens:
            values.append(str(token))
        return ' '.join(values)