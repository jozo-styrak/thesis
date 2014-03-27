from lib.frames.verb_frames.forms import CaseForm, InfinitiveForm
from lib.frames.verb_frames.attributes import DependencyAttribute, LemmaAttribute

# class representing slot in verbal frame
class AbstractSlot:

    def __init__(self):
        self.match_item = None
        self.obligatory = True
        self.dependent_on = 1

    def isObligatory(self):
        return self.obligatory

    def match(self, sentence):
        pass

    def testAttributes(self, phrase):
        fits = True
        for attribute in self.attributes:
            fits = fits and attribute.matchesWithPhrase(phrase)
        return fits

    # if value can be ellipsed
    def canBeEllipsed(self):
        return False

# verbal slot - basicly for now no attributes
class VerbSlot(AbstractSlot):

    def __init__(self):
        AbstractSlot.__init__(self)

    def __str__(self):
        return 'VERB'

# common slot
class CommonSlot(AbstractSlot):

    # in definition 3 obligatory parameters, and optional bracketed attributes
    def __init__(self, role_str, definition):
        AbstractSlot.__init__(self)
        def_elements = definition.split(';')
        # 1st level role
        self.first_level_role = role_str
        # form of the token, currently just case form with possible preposition
        self.form = InfinitiveForm() if def_elements[0].strip() == 'inf' else CaseForm(def_elements[0].strip())
        # second level role
        self.second_level_role = def_elements[1].strip()
        # obligatory?
        self.obligatory = False if def_elements[2].strip() == 'opt' else True
        # are there any attributes?
        self.attributes = []
        if len(def_elements) > 3:
            attrs = ';'.join(def_elements[3:])[1:-1].split(';')
            for attr in attrs:
                if attr.split(':')[0] == 'dependency':
                    self.attributes.append(DependencyAttribute(attr.split(':')[1]))
                elif attr.split(':')[0] == 'lemma':
                    self.attributes.append(LemmaAttribute(attr.split(':')[1]))

    # specified dependency of this attribute
    def dependentOn(self):
        dependency = 0
        for attribute in self.attributes:
            if isinstance(attribute, DependencyAttribute):
                dependency = attribute.value
        return dependency

    # whether given slot can be ellipsed
    # currently, slot with first role as AG or PAT can be ellipsed (zamlcany podmet)
    # that means, name of agency or stock does not have to be mentioned in given sentence
    def canBeEllipsed(self):
        return self.first_level_role == 'AG' or self.first_level_role == 'PAT'

    def __str__(self):
        attr_str = ''
        for attr in self.attributes:
            attr_str += str(attr) + ','
        return self.first_level_role + ' ' + self.second_level_role + ' ' + str(self.form) + ' ' + attr_str[:-1]
