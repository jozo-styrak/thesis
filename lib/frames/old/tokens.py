# from lib.sentence.phrases import VPhrase
# from lib.frames.token_attributes import CaseAttribute, LemmaAttribute, DependencyAttribute
#
# class Token:
#
#     def __init__(self, attributes):
#         self.match_item = None
#         self.attributes = []
#         self.obligatory = True
#         # reading the attributes
#         for attribute_str in attributes.strip().split(';'):
#             identificator = attribute_str.split(':')[0]
#             value = attribute_str.split(':')[1] if attribute_str.find(':') != -1 else ''
#             if identificator == 'case':
#                 self.attributes.append(CaseAttribute(value))
#             elif identificator == 'lemma':
#                 self.attributes.append(LemmaAttribute(value))
#             elif identificator == 'dependency':
#                 self.attributes.append(DependencyAttribute(value))
#             elif identificator == 'opt':
#                 self.obligatory = False
#             elif identificator == 'obl':
#                 self.obligatory = True
#
#     def match(self, sentence):
#         pass
#
#     def testAttributes(self, phrase):
#         fits = True
#         for attribute in self.attributes:
#             fits = fits and attribute.matchesWithPhrase(phrase)
#         return fits
#
#     def removeMatch(self):
#         self.match_item = None
#
#     def dependentOn(self):
#         dependency = 0
#         for attribute in self.attributes:
#             if isinstance(attribute, DependencyAttribute):
#                 dependency = attribute.value
#         return dependency
#
#     def isObligatory(self):
#         return self.obligatory
#
#     def __str__(self):
#         retValue = 'attributes: '
#         for attribute in self.attributes:
#             retValue += str(attribute) + ' '
#         return retValue
#
# class VerbToken(Token):
#
#     def __init__(self, attributes):
#         Token.__init__(self, attributes)
#
#     def match(self, sentence):
#         matches = False
#         i = 0
#         phrases = []
#         for clause in sentence.clauses:
#             for phrase in clause.phrases:
#                 phrases.append(phrase)
#         while not matches and i < len(phrases):
#             if isinstance(phrases[i], VPhrase):
#                 matches = self.testAttributes(phrases[i])
#             i += 1
#         if matches:
#             self.match_item = phrases[i-1]
#         return matches
#
#     def __str__(self):
#         return 'Verb -> ' + Token.__str__(self)
#
# class PhraseToken(Token):
#
#     def __init__(self, role, attributes):
#         Token.__init__(self, attributes)
#         self.role = role
#
#     def __str__(self):
#         return self.role + ' -> ' + Token.__str__(self)
#