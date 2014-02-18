import re
import sys
from levenstein_custom import *

fileHandle_formatted_story = open('story_no_punctuation.txt','w')
fileHandle_corrected_story = open('story_corrected_my_version.txt','w')
fileHandle = open('story.txt', 'r')

contents = fileHandle.read()

formatted_string = contents.replace('?', '').replace('.', '').replace(',', '').replace('"','').replace('!', '').replace('\n',' ').lower()
fileHandle_formatted_story.write(formatted_string)
fileHandle_formatted_story.close()

words = formatted_string.split()

fileHandle = open('dict.txt', 'r')
contents = fileHandle.read()
dictionary_words = contents.split()

for i in range(0,len(words)):

    [distance, dict_index] = levenshtein_distance(dictionary_words, words[i])
    words[i] = dictionary_words[dict_index]

fileHandle_corrected_story.write(' '.join(words))
fileHandle_corrected_story.close()


