#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filter texts from given directory to found matching string
# used for extraction of recommendation news from larger datasets
import sys

f = open(sys.argv[1].strip(),'r')
file_content = f.read().strip()

if file_content.find(sys.argv[2].strip()) != -1:
    print sys.argv[1], ' - MATCH FOUND!'
    print file_content
    print ""