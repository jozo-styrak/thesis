# module containing possible attributes for common slot

class TokenAttribute:

    def matchesWithPhrase(self, phrase):
        return True

    def __str__(self):
        return '{attribute}'

# attribute specifying lemma to match for given slot
class LemmaAttribute(TokenAttribute):

    def __init__(self, lemma_str):
        self.value = lemma_str

    # match method - is there in given phrase specified lemma?
    def matchesWithPhrase(self, phrase):
        found = False
        for token in phrase.tokens:
            if token.lemma == self.value:
                found = True
        return found

    def __str__(self):
        return '{lemma=' + str(self.value) + '}'

# attribute redefinies dependency for given slot
class DependencyAttribute(TokenAttribute):

    # positive number identifies slot in frame
    # -1 means, that dependency is unclear - for som prepositional phrase etc.
    def __init__(self, dependency_str):
        self.value = int(dependency_str)

    def __str__(self):
        dependency_str = 'verb'
        if self.value > 0:
            dependency_str = 'token ' + str(self.value)
        elif self.value < 0:
            dependency_str = 'unclear'
        return '{dependency=' + dependency_str + '}'