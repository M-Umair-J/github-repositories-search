import nltk
import os
import csv
from config import config
import ast
import sys


# increasing csv field size limit to ensure proper loading of data from csv files
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


current_dir = os.getcwd() # getting the current working directory
parent_dir = os.path.dirname(current_dir) # using the current working directory to get the parent directory

query = input("write the search\n")
query_list = nltk.word_tokenize(query)
lemmatizer = nltk.WordNetLemmatizer()
query_list = [lemmatizer.lemmatize(w) for w in query_list]
list_of_resuls = []
lexicon= {}
for i in query_list:
    i = i.lower()
    if i[0] in 'abcd':
        lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/A_to_D.csv', 'r')
        lex_reader = csv.DictReader(lex_file)
        for row in lex_reader:
            if i == row['words']:
                lexicon[row['id']] = row['words']
    elif i[0] in 'efgh':   
        lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/E_to_H.csv', 'r')
        lex_reader = csv.DictReader(lex_file)
        for row in lex_reader:
            if i == row['words']:
                lexicon[row['id']] = row['words']
    elif i[0] in 'ijkl':
        lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/I_to_L.csv', 'r')
        lex_reader = csv.DictReader(lex_file)
        for row in lex_reader:
            if i == row['words']:
                lexicon[row['id']] = row['words']
    elif i[0] in 'mnop':
        lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/M_to_P.csv', 'r')
        lex_reader = csv.DictReader(lex_file)
        for row in lex_reader:
            if i == row['words']:
                lexicon[row['id']] = row['words']
    elif i[0] in 'qrst':
        lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/Q_to_T.csv', 'r')
        lex_reader = csv.DictReader(lex_file)
        for row in lex_reader:
            if i == row['words']:
                lexicon[row['id']] = row['words']
    elif i[0] in 'uvwx':
        lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/U_to_X.csv', 'r')
        lex_reader = csv.DictReader(lex_file)
        for row in lex_reader:
            if i == row['words']:
                lexicon[row['id']] = row['words']
    elif i[0] in 'yz':
        lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/Y_to_Z.csv', 'r')
        lex_reader = csv.DictReader(lex_file)
        for row in lex_reader:
            if i == row['words']:
                lexicon[row['id']] = row['words']
    else:
        lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/Other.csv', 'r')
        lex_reader = csv.DictReader(lex_file)
        for row in lex_reader:
            if i == row['words']:
                lexicon[row['id']] = row['words']
    list_of_resuls.append(lexicon)


for i in list_of_resuls:
    total_partitions = config.get_total_partitions()
    partition = int(list(i.keys())[0])%total_partitions
    with open(parent_dir+'/repositoryData/invertedIndexBarrels/partition_'+str(partition)+'.csv', 'r') as inverted_index_file:
        inverted_index_reader = csv.DictReader(inverted_index_file)
        for row in inverted_index_reader:
            if list(i.keys())[0] == row['word_id']:
                doctList = ast.literal_eval(row['documents'])
                doctList = sorted(doctList.items(), key=lambda x: x[1], reverse=True)
                # docList = sortDict(doctList)
                break

for i in doctList:
    print(i[0])
    
