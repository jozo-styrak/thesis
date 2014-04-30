import copy

from lib.frames.verb_frames.slots import VerbSlot, CommonSlot
from lib.frames.verb_frames.forms import CaseForm
from lib.semantics.semantic_role import SemanticRole
from lib.semantics.semantic_relation import SemanticRelation
from lib.sentence.phrases import NPhrase
from lib.sentence.sentence import Token


# class containing one frame for given verb
class Frame:
    
    def __init__(self, slots):
        self.verb = None  # matching verb lemma from verb valence
        self.vp_match_item = None  # matching verb phrase from given clause
        # slot lists
        self.matched_slots = None  # link to matching slot list
        self.active_frame_slots = slots  # active slots of this frame
        self.passive_frame_slots = None  # passive frame slots
        # generate passive forms (if there is object in frame)
        if len(self.active_frame_slots) > 2: self.generatePassiveFrame()

    # generate passive frame from given slot tokens
    def generatePassiveFrame(self):
        self.passive_frame_slots = copy.deepcopy(self.active_frame_slots)  # rest should be the same
        self.passive_frame_slots[0].form = CaseForm('kym7')  # agens is in 7 case
        self.passive_frame_slots[2].form = CaseForm('co1')  # patiens is in 1 case

    # check whether given phrase is already matched with some token
    def isMatched(self, phrase):
        matched = False
        for slot in self.active_frame_slots:
            if slot.match_item != None and slot.match_item is phrase:
                matched = True
        return matched

    # return candidate phrases from clause to match given slot
    def getCandidatePhrases(self, clause, slot):
        if slot.dependentOn() == 0:  # if token needs phrase dependent on main verb
            return clause.getDependentPhrases(self.vp_match_item)
        elif slot.dependentOn() > 0:  # if token needs phrase dependent on another phrase
            return clause.getDependentPhrases(self.active_frame_slots[slot.dependentOn()-1].match_item)
        else:  # if dependency is unclear - returns all unmatched phrases -> mainly for preposition phrases with recommendations
            phrases = []
            for phr in clause.phrases:
                if not self.isMatched(phr):
                    phrases.append(phr)
            return phrases

    # check, whether valence verb is in passive in given phrase
    def isMatchVerbPassive(self):
        is_passive = False
        for token in self.vp_match_item.tokens:
            if token.lemma == self.verb:
                if 'mN' in token.tag:
                    is_passive = True
        return is_passive

    # set match item for this frame - tuple (lemma, verb phrase) as input
    def setMatchVerb(self, verb_tuple):
        self.verb = verb_tuple[0]
        self.vp_match_item = verb_tuple[1]

    # try to match self on the clause, returns
    def matchFrame(self, clause):
        # which frame slots to use?
        slots = self.active_frame_slots if not self.isMatchVerbPassive() else self.passive_frame_slots
        failed = False
        i = 0
        # try to find matches for frame slots
        while not failed and i < len(slots):
            phrase_matches = False
            if isinstance(slots[i], VerbSlot):  # for now, just set match item for verb slot
                slots[i].match_item = self.vp_match_item
                phrase_matches = True
            else:  # find matching phrase for common slot
                for phrase in self.getCandidatePhrases(clause, slots[i]):  # search in candidate phrases based on dependency of given slot
                    if not self.isMatched(phrase) and not phrase_matches and slots[i].form.matchPhrase(phrase) and slots[i].testAttributes(phrase):
                        slots[i].match_item = phrase
                        phrase_matches = True
            # fail if match was not found and slot is obligatory and can't be ellipsed
            failed = (not phrase_matches) and slots[i].isObligatory() and not slots[i].canBeEllipsed()
            i += 1

        # generate semantic relation and occupy given roles
        # relation = SemanticRelation() if not failed else None
        # newer version - if clause already has relation, use this
        if not failed:
            if clause.containing_relation == None:
                clause.containing_relation = SemanticRelation()
                clause.containing_relation.containing_clause = clause
            self.matched_slots = slots
            for slot in self.matched_slots:
                # create role for every occupied slot and for slot, which is ellipsable
                # check if given phrase already has given role
                if isinstance(slot, CommonSlot) and (slot.match_item != None or slot.canBeEllipsed()) and ((slot.match_item == None and slot.canBeEllipsed()) or (slot.match_item != None and not slot.match_item.hasRole(slot.second_level_role))):
                    role = SemanticRole(slot.first_level_role, slot.second_level_role)
                    if slot.match_item != None:
                        # set role phrase
                        role.setPhrase(slot.match_item)
                        # set link to role into phrase
                        slot.match_item.semantic_roles.append(role)
                    # ellipsed WE agens
                    elif self.vp_match_item.hasTag('p1') and 'actor' in slot.second_level_role and 'AG' in slot.first_level_role:
                        we_phrase = NPhrase('k1gInPc1', '0', '0', False)
                        # we_phrase.tokens.append(Token('Fio_kA', 'Fio_kA', 'k1gInPc1'))
                        we_phrase.tokens.append(Token('Fio_STATE', 'Fio', 'k1gInPc1'))
                        clause.phrases.append(we_phrase)
                        role.setPhrase(we_phrase)
                        we_phrase.semantic_roles.append(role)
                    # don't add new ellipsed role
                    if role.phrase != None or (role.phrase == None and not clause.containing_relation.hasEllipsedRole(slot.second_level_role)):
                        clause.containing_relation.addNewRole(role)
        # return clause.containing_relation

    # after matching remove matched items
    def resetFrame(self):
        self.verb = None
        self.vp_match_item = None
        for slot in self.active_frame_slots:
            slot.match_item = None
        
    def __str__(self):
        slot_str = ''
        verb_str = '' if self.verb == None else 'verb ' + self.verb + ' : '
        for slot in self.active_frame_slots:
            slot_str += str(slot) + ' | '
        return '<frame> ' + verb_str + slot_str[:-3] + ' </frame>'