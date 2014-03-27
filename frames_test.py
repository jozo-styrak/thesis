from lib.frames.verb_frames.verb_frame_matcher import VerbFrameMatcher

f = open('frames/frames.data', 'r')
frame_matcher = VerbFrameMatcher(f)
frame_matcher.printFrames()