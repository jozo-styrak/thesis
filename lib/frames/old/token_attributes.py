# from lib.sentence.phrases import NPhrase
#
#
# class TokenAttribute:
#     def matchesWithPhrase(self, phrase):
#         return True
#
#
# class CaseAttribute(TokenAttribute):
#     def __init__(self, case_str):
#         self.value = case_str.strip().split('|')[0]
#         self.abbreviation = True if case_str.find('kA') != -1 else False
#
#     def matchesWithPhrase(self, phrase):
#         if isinstance(phrase, NPhrase):
#             if str(phrase.case) == self.value or (phrase.case == 0 and self.abbreviation):
#                 return True
#             else:
#                 return False
#         else:
#             return False
#
#     def __str__(self):
#         return '{case=' + self.value + ', abbreviation?=' + str(self.abbreviation) + '}'
#
#
# class LemmaAttribute(TokenAttribute):
#     def __init__(self, lemma_str):
#         self.value = lemma_str
#
#     def matchesWithPhrase(self, phrase):
#         found = False
#         for token in phrase.tokens:
#             if token.lemma == self.value:
#                 found = True
#         return found
#
#     def __str__(self):
#         return '{lemma=' + str(self.value) + '}'
#
#
# class DependencyAttribute(TokenAttribute):
#     def __init__(self, dependency_str):
#         self.value = int(dependency_str)
#
#     def __str__(self):
#         dependency_str = 'verb'
#         if self.value > 0:
#             dependency_str = 'token ' + str(self.value)
#         elif self.value < 0:
#             dependency_str = 'unclear'
#         return '{dependency=' + dependency_str + '}'