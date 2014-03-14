# class representing one verb (or group of verbs with same meaning)
# contains corresponding verbal frames
class FrameVerb:

    def __init__(self, verbs_str):
        self.verbs = []
        for verb in verbs_str.split(';'):
            self.verbs.append(verb.strip())
        self.frames = []

    # tries to match one of the verbs with verbs from given clause, returns tuple of verb and verb phrase if succeeded
    def inClause(self, clause):
        matches = None
        for verb_phrase in clause.getVPhrases():
            for token in verb_phrase.tokens:
                if token.lemma in self.verbs:
                    matches = (token.lemma, verb_phrase)
        return matches

    # main matching method
    def matchClause(self, clause):
        vp_match = self.inClause(clause)
        if vp_match != None:  # does the verb match?
            matches = []
            for frame in self.frames:  # try to pass on verbal frames
                frame.setMatchVerb(vp_match)  # set matching lemma from valence verbs and matching phrase from clause
                if frame.matchFrame(clause):
                    matches.append(frame)
            return matches
        else:
            return []

    # after matching, reset matched items
    def resetFrames(self):
        for frame in self.frames:
            frame.resetFrame()

    def __str__(self):
        frames_str = ''
        for frame in self.frames:
            frames_str += str(frame) + '\n'
        return 'Verbs: ' + ', '.join(self.verbs) + '\n' + frames_str