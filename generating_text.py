# -*- coding: utf8 -*-

from __future__ import with_statement
import json
import cPickle as pickle
import random
import os
import sys
import re
from collections import defaultdict

supp_delimiters = ['.', ',', '!', '?', ' ']   
max_sentences = 5

def is_correct_input():
    if len(sys.argv) != 6:
        print 'Whong number of input argument'
        print 'First argument: path to output_file'
        print 'Second argument: required_text_length'
        print '3rd: Path to first_dump_file'
        print '4th: Path to second_dump_file'
        print '5th: Path to third_dump_file'
        exit(-1)

def weighted_choice(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i
    return 0        

def get_by_one(prevw, one_word_corr):
    variants = []
    weights = []
    for key, value in one_word_corr.iteritems():
        variants.append(key)
        weights.append(value)
    if (len(variants) == 0):
        return '$'        
    return variants[weighted_choice(weights)]

def get_by_two(preprevw, prevw, two_words_corr):
    variants = []
    weights = []
    for key, value in two_words_corr.iteritems():
        variants.append(key)
        weights.append(value)
    if (len(variants) == 0):
        return '$'        
    return variants[weighted_choice(weights)]

def generate_text(required_text_length, one_word_corr, two_words_corr, sentence_starters):
    answer = ''
    prevw = ''
    preprevw = ''
    previous_delimiter = ''
    length = 0
    current_sentence_length = 0
    current_number_of_delimiters = 0
    while (length < required_text_length):
        print length
        if (current_sentence_length == 0):
            first_word = random.choice(sentence_starters)
            answer += ' '
            if (previous_delimiter != ','):
                answer += first_word.title()
            else:
                answer += first_word   
            prevw = first_word
        
        if (current_sentence_length == 1):    
            next_word = get_by_one(prevw, one_word_corr[prevw])
            if next_word != '$':
                if (next_word not in supp_delimiters):
                    answer += ' '
                answer += next_word
                preprevw = prevw
                prevw = next_word
        
        if (current_sentence_length > 1):
            next_word = get_by_two(preprevw, prevw, two_words_corr[preprevw][prevw])
            if next_word != '$':
                if (next_word not in supp_delimiters):
                    answer += ' '
                answer += next_word
                preprevw = prevw
                prevw = next_word

        current_sentence_length += 1
        length += 1
        if (prevw in supp_delimiters):
            current_number_of_delimiters += 1
            current_sentence_length = 0
            previous_delimiter = prevw
            prevw = ''
            preprevw = ''   

        if (current_number_of_delimiters > max_sentences and previous_delimiter != ','):
            current_number_of_delimiters = 0
            answer += '\n\n'


    return answer

with open(sys.argv[3], 'r') as fp:
    one_word_corr = json.load(fp)

with open(sys.argv[4], 'r') as fp:
    two_words_corr = json.load(fp)

with open(sys.argv[5], 'r') as fp:
    sentence_starters = json.load(fp)         

required_text_length = int(sys.argv[2])
with open(sys.argv[1], 'w') as output_file:
    output_file.write(generate_text(required_text_length, 
        one_word_corr, two_words_corr, sentence_starters))        