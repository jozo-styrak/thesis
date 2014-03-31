#!/usr/bin/env python
''' file contains class declarations for sentence analysis '''
''' includes classes for set processing with aided semantic information from verbalex '''


# Classes representing sentence structure
class Clause:

    def __init__(self, num, conj):
        self.num = num
        self.conj = conj
        self.phrases = []

    # return whether phrase with specified numeric representation is part of the clause
    def inClause(self, phr_num):
        inClause = True
        for num in phr_num.split():
            if not num in self.num.split():
                inClause = False
        return inClause

    # if clause contains verb
    def containsVerbPhrase(self):
        contains = False
        for phrase in self.phrases:
            if isinstance(phrase, VPhrase):
                contains = True
        return contains

    # returns the verb phrase list from this clause
    def getVPhrases(self):
        phr = []
        for phrase in self.phrases:
            if isinstance(phrase, VPhrase):
                phr.append(phrase)
        return phr

    # returns nps that succeeds given phrase
    def getSucceedingPhrases(self, phrase):
        return self.phrases[self.phrases.index(phrase)+1:]

    # return phrases which are dependent on specified phrase
    def getDependentPhrases(self, phrase):
        dependent = []
        for phr in self.phrases:
            if isinstance(phr, NPhrase) and phrase is phr.dependent_on:
                dependent.append(phr)
        return dependent


# classes representing phrases generated by set
# list tokens contains pointers to tokens contained by sentence and are added in creation of phrase in addNewPhrase()
class Phrase:

    def __init__(self, num, head):
        self.num =  num
        self.head = head
        self.tokens = []
        self.semantic_roles = []

    # add semantic role
    def addSemanticRole(self, role):
        self.semantic_roles.append(role)

    # check, whether phrase has given role
    # if base role is found, then upgrade the role
    def hasRole(self, role_str):
        has = False
        for role in self.semantic_roles:
            if role_str == role.second_level_role:
                has = role
            elif '_' in role_str and not '_' in role.second_level_role and role_str[1:-3].split('_')[0] == role.second_level_role[1:-3]:
                role.second_level_role = role_str
                has = role
            elif '_' in role.second_level_role and not '_' in role_str and role.second_level_role[1:-3].split('_')[0] == role_str[1:-3]:
                has = role
        return has

    # check whether there is conflict with given role
    # for now, conflicts are in group of kA roles, agency, stock, organization
    # def roleConflict(self, role_str):
    #     conflict = False
    #     if (self.hasRole('<agency:1>') and (role_str == '<stock:1>' or role_str == '<organization:1>')) or (self.hasRole('<stock:1>') and (role_str == '<agency:1>' or role_str == '<organization:1>')) or (self.hasRole('<organization:1>') and (role_str == '<agency:1>' or role_str == '<stock:1>')):
    #         conflict = True
    #     return conflict

    # new role conflict method - syntax base_specific for role name
    # conflict between specific roles
    def roleConflict(self, role_str):
        conflict = False
        for role in self.semantic_roles:
            if '_' in role.second_level_role and '_' in role_str and role.second_level_role[1:-3].split('_')[0] == role_str[1:-3].split('_')[0] and role.second_level_role[1:-3].split('_')[1] != role_str[1:-3].split('_')[1]:
                conflict = True
        return conflict
    
    def __str__(self):
        values = []
        for token in self.tokens:
            values.append(token.value)
        # semantics = ''
        # for role in self.semantic_roles:
        #     semantics += str(role)
        return ' '.join(values)

class VPhrase(Phrase):

    def __init__(self, num, head):
        Phrase.__init__(self, num, head)
        
    def __str__(self):
        retValue = 'Verb: ' + Phrase.__str__(self)
        return retValue
        
class NPhrase(Phrase):

    def __init__(self, tag, num, head, is_coord):
        Phrase.__init__(self, num, head)
        self.case = int(tag[tag.find('c')+1]) if tag.split()[0].find('c') != -1 else 0
        self.dependent_on = None
        self.is_coordination = is_coord

    # check whether phrase is part of coordination
    def isInCoordination(self):
        return False if self.dependent_on == None else isinstance(self.dependent_on, NPhrase) and self.dependent_on.is_coordination
        
    def __str__(self):
        ret_value = 'Case ' + str(self.case) + ': ' + Phrase.__str__(self)
        if self.dependent_on != None:
            ret_value += ' ->>> ' + str(self.dependent_on.head)
        return ret_value

