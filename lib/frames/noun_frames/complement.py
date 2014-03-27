from lib.frames.verb_frames.forms import CaseForm

# class representing noun complement
# consists of case form and role string
class Complement:

    def __init__(self, id_str):
        values = id_str.split(';')
        self.case_form = CaseForm(values[0])
        self.role = values[1]
        self.matched = False

    # if given phrase matches
    def matchPhrase(self, phrase):
        self.matched = self.case_form.matchPhrase(phrase)
        return self.matched

    def __str__(self):
        return '{form: ' + str(self.case_form) + ', role: ' + self.role + '}'