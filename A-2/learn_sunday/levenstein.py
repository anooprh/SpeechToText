import numpy as np
import node_element

def levenshtein_simple(string1,string2):
    if len(string1) > len(string2):
        string1,string2 = string2,string1
    distances = range(len(string1) + 1)
    for index2,char2 in enumerate(string2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(string1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]

# print(levenshteinDistance("t","sitting"))
# print(levenshteinDistance("rosettacode","raisethysword"))

if __name__ =="__main__":
    levenshtein_simple("abc", "def")