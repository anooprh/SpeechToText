from levenstein_string_prune import *

fileHandle_story_correct_no_punctuation = open('story_correct_no_punctuation.txt','w')
fileHandle_story_corrected_my_version = open('story_corrected_my_version.txt','r')
fileHandle_storycorrect = open('storycorrect.txt', 'r')
fileHandle_story_no_punctuation = open('story_no_punctuation.txt', 'r')

contents = fileHandle_storycorrect.read()

formatted_string = contents.replace('?', '').replace('.', '').replace(',', '').replace('"','').replace('!', '').replace('\n',' ').lower()

fileHandle_story_correct_no_punctuation.write(formatted_string)
fileHandle_story_correct_no_punctuation.close()

original_formatted = fileHandle_story_no_punctuation.read()
corrected_string = fileHandle_story_corrected_my_version.read()

fileHandle_story_correct_no_punctuation = open('story_correct_no_punctuation.txt','r')
correct_story = fileHandle_story_correct_no_punctuation.read()

print "Distance between original story and its corrected version"
print levenshtein_distance(original_formatted, correct_story)

print "Distance between my version of correct story and its corrected version"
print levenshtein_distance(corrected_string, correct_story)

fileHandle_story_correct_no_punctuation.close()
fileHandle_story_corrected_my_version.close()
fileHandle_storycorrect.close()
fileHandle_story_no_punctuation.close()
