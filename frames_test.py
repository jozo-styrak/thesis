from lib.frames.frame_matcher import FrameMatcher

f = open('data/patterns.data', 'r')
frame_matcher = FrameMatcher(f)
frame_matcher.printFrames()