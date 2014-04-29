import re

# static class for resolving actor roles
class RoleResolver:

    @staticmethod
    def resolveActorRoles(relations, sentences):
        for relation in relations:
            for role in relation.roles:
                if role.second_level_role == '<actor:1>' and role.phrase != None:

                    # rules:
                    # is there word 'akcie', 'titul', ...? or 'agentura'
                    if RoleResolver.wordPresenceRule(role.phrase, ['akcie', 'akcia', 'titul']):
                        role.second_level_role = '<actor_stock:1>'
                    elif RoleResolver.wordPresenceRule(role.phrase, ['agentura']):
                        role.second_level_role = '<actor_agency:1>'
                    # is there parenthesis with price value?
                    elif RoleResolver.parenthesisRule(role.phrase):
                        role.second_level_role = '<actor_stock:1>'
                    # is there another same-named entity in text?
                    elif RoleResolver.alreadyInTextRule(role, relations, True):
                        # role is assigned in method
                        pass
                    # is name followed in text with ':'?
                    elif RoleResolver.sameClauseRule(role, True):
                        # role is assigned in method
                        pass
                    # no rule applies, leave unresolved
                    elif RoleResolver.followTokenRule(role.phrase, sentences, [':', '-']):
                        role.second_level_role = '<actor_agency:1>'
                    # is name followed in text with '-'?
                    # elif RoleResolver.followTokenRule(role.phrase, sentences, ['-']):
                    #     role.second_level_role = '<actor_stock:1>'
                    # is there already another entity of same role in given clause?
                    else:
                        pass

    # checks for presence of given lemmas within phrase
    @staticmethod
    def wordPresenceRule(phrase, word_lemmas):
        present = False
        for token in phrase.tokens:
            if token.lemma in word_lemmas:
                present = True
        return present

    # checks for presence of numbered value in parenthesis
    @staticmethod
    def parenthesisRule(phrase):
        joined_tokens = ''
        for token in phrase.tokens:
            joined_tokens += token.value
        return RoleResolver.containsPriceValue(joined_tokens)

    # sub method for presence of parenthesised numeric value in STRING representation
    @staticmethod
    def containsPriceValue(entity_str):
        PRICE_PATTERN = re.compile('.*_[\+-]*\d+[\.,/:]*\d*_.*')
        return PRICE_PATTERN.match(entity_str)

    # checks for presence of given named entity in text
    # if assign set to true, changes role to given
    @staticmethod
    def alreadyInTextRule(role, relations, assign):
        entity_name = None
        assigned = False
        for token in role.phrase.tokens:
            if token.value.endswith('ACTOR'):
                entity_name = token.value[:-6]
        if entity_name != None:
            # find same named entity
            for relation in relations:
                for r in relation.roles:
                    if r.phrase != role.phrase and r.phrase != None and r.second_level_role.startswith('<actor_'):
                        contains = False
                        for token in r.phrase.tokens:
                            if entity_name in token.value:
                                contains = True
                            # for now, full name must match
                            if contains:
                                # potentionally change role
                                if assign:
                                    role.second_level_role = r.second_level_role
                                assigned = True
        return assigned

    # checks for phrase following token
    @staticmethod
    def followTokenRule(phrase, sentences, tokens):
        contains = False
        sentence = None
        for sent in sentences:
            for clause in sent.clauses:
                for phr in clause.phrases:
                    if phr == phrase:
                        sentence = sent
        # following_token = sentence.getFollowingTokenToPhrase(phrase)
        token = None
        for t in phrase.tokens:
            if t.value.endswith('ACTOR'):
                token = t
        following_token = sentence.getFollowingTokenToToken(token)
        if following_token != None and following_token.value in tokens:
            contains = True
        return  contains

    # if there is already given role in sentence, then this has probably different role
    # if assign set to true, changes role to given
    @staticmethod
    def sameClauseRule(role, assign):
        assigned = False
        for r in role.relation.roles:
            if r != role and r.second_level_role.startswith('<actor_') and r.coreferent != None:
                if r.second_level_role == '<actor_agency:1>':
                    # if assign set to true, changes role to given
                    if assign:
                        role.second_level_role = '<actor_stock:1>'
                    assigned = True
                elif r.second_level_role == '<actor_stock:1>':
                    # if assign set to true, changes role to given
                    if assign:
                        role.second_level_role = '<actor_agency:1>'
                    assigned = True
        return assigned

    # check for relevancy
    # False, when some of non-agency criteria applies, otherwise True
    @staticmethod
    def isRelevantAgencyEntity(entity_str):
        # can not be agency, if there is a price entity
        relevant = True
        if RoleResolver.containsPriceValue(entity_str):
            relevant = False
        return relevant

