#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PipelineUtils:

    # from list of sentences buffer lines for each sentence
    # outputs list of sentences, where sentence is list of triples [token, lemma, tag] representing words
    @staticmethod
    def bufferSentences(lines):
        sentences = []
        i = 0
        while i < len(lines):
            if lines[i].startswith('<s'):
                sentence = []
                i += 1
                while not lines[i].startswith('</s>'):
                    sentence.append(lines[i].strip().split())
                    i += 1
                sentences.append(sentence)
            i += 1
        return sentences

    # format output into desamb type format
    # connects triples [token, lemma, tag] into string output
    @staticmethod
    def formatDesambOutput(sentences):
        i = 1
        for sentence in sentences:
            print '<s desamb=\"',i,'\">'
            for word in sentence:
                print '\t'.join(word)
            print "</s>"
            i += 1

    # method for connecting objects inside parenthesis
    @staticmethod
    def connectParenthesis(tokens):
        # execute this method only if there is even count of parethesis
        count = 0
        for token in tokens:
            if token[0] == '(' or token[0] == ')':
                count += 1
        if count == 0 or count % 2 == 1:
            return tokens
        else:
            # connect object in parenthesis
            start = False
            new_tokens = []
            parenthesis_content = ['','','kA']
            for token in tokens:
                if not start and token[0] != '(':
                    new_tokens.append(token)
                elif not start and token[0] == '(':
                    start = True
                    parenthesis_content[0] = '('
                    parenthesis_content[1] = '('
                elif start and token[0] != ')':
                    parenthesis_content[0] += '_' + token[0]
                    parenthesis_content[1] += '_' + token[1]
                elif start and token[0] == ')':
                    parenthesis_content[0] += '_)'
                    parenthesis_content[1] += '_)'
                    new_tokens.append(parenthesis_content)
                    parenthesis_content = ['','','kA']
                    start = False
            return new_tokens

    # connect quotes -  everything inside is tagged as kA
    # for recommendations
    @staticmethod
    def connectQuotes(tokens):
        # execute this method only if there is even count of quotes
        quote_count = 0
        for token in tokens:
            if token[0] == '\"':
                quote_count += 1
        if quote_count == 0 or quote_count % 2 == 1:
            return tokens
        else:
            # connect object in quotes
            quote_start = False
            new_tokens = []
            quote_content = ['','','kA']
            for token in tokens:
                if not quote_start and token[0] != '\"':
                    new_tokens.append(token)
                elif not quote_start and token[0] == '\"':
                    quote_start = True
                elif quote_start and token[0] != '\"':
                    quote_content[0] = quote_content[0] + '_' + token[0] if quote_content[0] != '' else token[0]
                    quote_content[1] = quote_content[1] + '_' + token[1] if quote_content[1] != '' else token[1]
                elif quote_start and token[0] == '\"':
                    # BONUS! if quote content is not in recommendations, add it there
                    # if not quote_content[0].lower() in RECOMMENDATIONS:
                    #     RECOMMENDATIONS.append(quote_content[0].lower())
                    new_tokens.append(quote_content)
                    quote_content = ['','','kA']

                    quote_start = False

            return new_tokens
