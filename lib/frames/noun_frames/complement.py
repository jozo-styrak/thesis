from lib.frames.verb_frames.forms import CaseForm

# class representing noun complement
# consists of case form and role string
class Complement:

    # id_str format AG(form;<sec_lvl_role>;obl)
    def __init__(self, id_str):
        self.first_level_role = id_str[:id_str.find('(')]
        values = id_str[id_str.find('('):][1:-1].split(';')
        self.case_form = CaseForm(values[0])
        self.second_level_role = values[1]
        self.obligatory = True if values[2] == 'obl' else False
        self.matched = False

    # if given phrase matches
    def matchPhrase(self, phrase):
        self.matched = self.case_form.matchPhrase(phrase)
        return self.matched

    # return whether complement is obligatory and therefore can be ellipsed and later resolved
    def isObligatory(self):
        return  self.obligatory

    def __str__(self):
        return '{form: ' + str(self.case_form) + ', role: ' + self.second_level_role + '}'