import nltk
import os
import csv
from config import config
import ast
import sys
import time
import threading

total_partitions = config.get_total_partitions()

def find_the_word_ids(words):
    lexicon = {}
    lexicon_word_to_id = {}
    
    # Load lexicon barrels into memory
    lexicon_files = {
        'A_to_D': 'repositoryData/lexicon_barrels/A_to_D.csv',
        'E_to_H': 'repositoryData/lexicon_barrels/E_to_H.csv',
        'I_to_L': 'repositoryData/lexicon_barrels/I_to_L.csv',
        'M_to_P': 'repositoryData/lexicon_barrels/M_to_P.csv',
        'Q_to_T': 'repositoryData/lexicon_barrels/Q_to_T.csv',
        'U_to_X': 'repositoryData/lexicon_barrels/U_to_X.csv',
        'Y_to_Z': 'repositoryData/lexicon_barrels/Y_to_Z.csv',
        'Other': 'repositoryData/lexicon_barrels/Other.csv',
    }

    for barrel, file_path in lexicon_files.items():
        with open(os.path.join(parent_dir, file_path), 'r', encoding='utf-8') as lex_file:  # Specify utf-8 encoding
            lex_reader = csv.DictReader(lex_file)
            for row in lex_reader:
                if row['words'].lower() in words:
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
        maxInt = int(maxInt / 10)

current_dir = os.getcwd()  # getting the current working directory
parent_dir = os.path.dirname(current_dir)  # using the current working directory to get the parent directory
lemmatizer = nltk.WordNetLemmatizer()

characters_of_interest = ['/', ',', '.', '-', '_']
query = input("write the search\n")

# Clean the query
broken_query = query
for char in characters_of_interest:
    if char in query:
        broken_query = broken_query.replace(char, ' ')

# Tokenize and lemmatize the query
broken_query = broken_query.split()
lemmatized_broken_query = [lemmatizer.lemmatize(i.lower()) for i in broken_query]

query_list = nltk.word_tokenize(query)
query_list = [lemmatizer.lemmatize(w) for w in query_list]

# Merge the broken query and tokenized query into one list, removing duplicates
final_query_list = list(set(query_list + lemmatized_broken_query))

# Find word ids from the lexicon
lexicon, lexicon_word_to_id = find_the_word_ids(final_query_list)

# Process results from the inverted index
finalList = []
for word_id in lexicon:
    partition = int(word_id) % total_partitions
    doctList = []

    # Open the partition file for the specific partition
    partition_file_path = os.path.join(parent_dir, f'repositoryData/invertedIndexBarrels/partition_{partition}.csv')
    
    with open(partition_file_path, 'r', encoding='utf-8') as inverted_index_file:
        inverted_index_reader = csv.DictReader(inverted_index_file)
        for row in inverted_index_reader:
            if word_id == row['word_id']:
                doctList = ast.literal_eval(row['documents'])
                break

    # Add the sorted documents to the final list
    for doc in doctList:
        finalList.append(doc)

# Output the final result
for doc in finalList:
    print(doc[0])
