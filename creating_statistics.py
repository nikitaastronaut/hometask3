# -*- coding: utf8 -*-

from __future__ import with_statement
import json
import random
import os
import sys
import re
from collections import defaultdict

supp_delimiters = ['.', ',', '!', '?', ' ']   
max_sentences = 5

def is_correct_input():
    if len(sys.argv) != 5:
        print 'Whong number of input argument'
        print 'First argument: path to the text corpus'
        print 'Second argument: path to dump_file_one'
        print 'Third argument: path to dump_file_two'
        print 'Fourth argument: path to dump_file_three'
        exit(-1)

def clean(line):
    delimiters_to_space = ['\n', '-']
    for delimiter in delimiters_to_space:
        re.sub(delimiter, ' ', line)

    line = filter(lambda c: (c.isalpha()) or ((c in supp_delimiters)), line)

    for delimiter in supp_delimiters:
        line = line.replace(delimiter.decode('utf8'), ' ' + delimiter + ' ')
    " ".join(line.split())


    return line.lower().encode('utf8')

def if_no_delimiters(words, w_idx, max_offset):
    for offset in range(0, max_offset):
        if words[w_idx + offset] in supp_delimiters:
            return False
    return True        

def get_statistics(path_to_corpus):
    one_word_corr = defaultdict(dict)
    two_words_corr = defaultdict(lambda: defaultdict(dict))
    sentence_starters = []
    sentence_lengths = []
    total_number_of_words = 0
    for path, dirs, files in os.walk(path_to_corpus): 
        for filename in files:
            fullpath = os.path.join(path, filename)
            with open(fullpath, 'r') as current_file:
                text = clean(current_file.read().decode('utf8'))
                words = text.split()
                total_number_of_words += len(words)
                sentence_length = 0
                for w_idx in range(0, len(words) - 1):
                    if (words[w_idx] in supp_delimiters and words[w_idx + 1] 
                        not in supp_delimiters and words[w_idx] != ','):
                        sentence_starters.append(words[w_idx + 1])           

                for w_idx in range(0, len(words) - 1):
                    if (if_no_delimiters(words, w_idx, 1)):
                        if (words[w_idx] in one_word_corr and 
                            words[w_idx + 1] in one_word_corr[words[w_idx]]):
                            one_word_corr[words[w_idx]][words[w_idx + 1]] += 1
                        else:
                            one_word_corr[words[w_idx]][words[w_idx + 1]] = 1         

                for w_idx in range(0, len(words) - 2):
                    if (if_no_delimiters(words, w_idx, 2)):
                        if (words[w_idx] in two_words_corr and 
                            words[w_idx + 1] in two_words_corr[words[w_idx]] 
                            and words[w_idx + 2] in two_words_corr[words[w_idx]][words[w_idx + 1]]):
                           two_words_corr[words[w_idx]][words[w_idx + 1]][words[w_idx + 2]] += 1
                        else:
                            two_words_corr[words[w_idx]][words[w_idx + 1]][words[w_idx + 2]] = 1
    print total_number_of_words                        
    return one_word_corr, two_words_corr, sentence_starters                                 

is_correct_input()
one_word_corr, two_words_corr, sentence_starters = get_statistics(sys.argv[1])

with open(sys.argv[2], 'w') as fp:
    json.dump(one_word_corr, fp) 

with open(sys.argv[3], 'w') as fp:
    json.dump(two_words_corr, fp)

with open(sys.argv[4], 'w') as fp:
    json.dump(sentence_starters, fp) 
