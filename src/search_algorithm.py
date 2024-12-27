import nltk
import os
import csv
from config import config
import ast
import sys

total_partitions = config.get_total_partitions()

def find_the_word_ids(words):
    lexicon= {}
    lexicon_word_to_id = {}
    for i in words:
        i = i.lower()
        if i[0] in 'abcd':
            lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/A_to_D.csv', 'r')
            lex_reader = csv.DictReader(lex_file)
            for row in lex_reader:
                if i == row['words']:
                    lexicon[row['id']] = row['words']
                    lexicon_word_to_id[row['words']] = row['id']
        elif i[0] in 'efgh':   
            lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/E_to_H.csv', 'r')
            lex_reader = csv.DictReader(lex_file)
            for row in lex_reader:
                if i == row['words']:
                    lexicon[row['id']] = row['words']
                    lexicon_word_to_id[row['words']] = row['id']

        elif i[0] in 'ijkl':
            lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/I_to_L.csv', 'r')
            lex_reader = csv.DictReader(lex_file)
            for row in lex_reader:
                if i == row['words']:
                    lexicon[row['id']] = row['words']
                    lexicon_word_to_id[row['words']] = row['id']

        elif i[0] in 'mnop':
            lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/M_to_P.csv', 'r')
            lex_reader = csv.DictReader(lex_file)
            for row in lex_reader:
                if i == row['words']:
                    lexicon[row['id']] = row['words']
                    lexicon_word_to_id[row['words']] = row['id']

        elif i[0] in 'qrst':
            lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/Q_to_T.csv', 'r')
            lex_reader = csv.DictReader(lex_file)
            for row in lex_reader:
                if i == row['words']:
                    lexicon[row['id']] = row['words']
                    lexicon_word_to_id[row['words']] = row['id']

        elif i[0] in 'uvwx':
            lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/U_to_X.csv', 'r')
            lex_reader = csv.DictReader(lex_file)
            for row in lex_reader:
                if i == row['words']:
                    lexicon[row['id']] = row['words']
                    lexicon_word_to_id[row['words']] = row['id']

        elif i[0] in 'yz':
            lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/Y_to_Z.csv', 'r')
            lex_reader = csv.DictReader(lex_file)
            for row in lex_reader:
                if i == row['words']:
                    lexicon[row['id']] = row['words']
                    lexicon_word_to_id[row['words']] = row['id']

        else:
            lex_file = open(parent_dir+'/repositoryData/lexicon_barrels/Other.csv', 'r')
            lex_reader = csv.DictReader(lex_file)
            for row in lex_reader:
                if i == row['words']:
                    lexicon[row['id']] = row['words']
                    lexicon_word_to_id[row['words']] = row['id']
    return lexicon, lexicon_word_to_id


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
lemmatizer = nltk.WordNetLemmatizer()
characters_of_interest = ['/',',','.','-','_']
query = input("write the search\n")
broken_query = query
for i in characters_of_interest:
    if i in query:
        broken_query = broken_query.replace(i, ' ')

broken_query = broken_query.split()
lemmatized_broken_query = []
for i in broken_query:
    lemmatized_broken_query.append(lemmatizer.lemmatize(i.lower()))

query_list = nltk.word_tokenize(query)
query_list = [lemmatizer.lemmatize(w) for w in query_list]

for i in lemmatized_broken_query:
    query_list.append(i)

list_of_resuls = []
lexicon= {}
lexicon_word_to_id = {}
lexicon,lexicon_word_to_id = find_the_word_ids(query_list)

finalList = []
for i in lexicon:
    partition = int(i)%total_partitions
    doctList = []
    with open(parent_dir+'/repositoryData/invertedIndexBarrels/partition_'+str(partition)+'.csv', 'r') as inverted_index_file:
        inverted_index_reader = csv.DictReader(inverted_index_file)
        for row in inverted_index_reader:
            if i == row['word_id']:
                doctList = ast.literal_eval(row['documents'])
                doctList = sorted(doctList.items(), key=lambda x: x[1], reverse=True)
                break

        for i in doctList:
            finalList.append(i)

for i in finalList:
    print(i[0])