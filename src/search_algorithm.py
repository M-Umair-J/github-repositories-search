import nltk
import os
import csv
from config import config
import ast
import sys
import time
# from server import load_important_stuff

lemmatizer = nltk.WordNetLemmatizer()
total_partitions = config.get_total_partitions()

current_dir = os.getcwd() # getting the current working directory
parent_dir = os.path.dirname(current_dir) # using the current working directory to get the parent directory

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

def search(query):
    # increasing csv field size limit to ensure proper loading of data from csv files
    maxInt = sys.maxsize
    while True:
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)

    
    characters_of_interest = ['/',',','.','-','_']

    broken_query = query
    for i in characters_of_interest:
        if i in query:
            broken_query = broken_query.replace(i, ' ')
    if(not(broken_query == query)):
        broken_query = broken_query.split()
        lemmatized_broken_query = []
        for i in broken_query:
            lemmatized_broken_query.append(lemmatizer.lemmatize(i.lower()))
        lexicon_for_broken_query = {}
        lexicon_word_to_id_for_broken_query = {}

        lexicon_for_broken_query, lexicon_word_to_id_for_broken_query = find_the_word_ids(lemmatized_broken_query)

    query_list = nltk.word_tokenize(query)
    query_list = [lemmatizer.lemmatize(w) for w in query_list]
    lexicon= {}
    lexicon_word_to_id = {}

    lexicon, lexicon_word_to_id = find_the_word_ids(query_list)
    



    finalList = {}
    for i in lexicon:
        partition = int(i)%total_partitions
        doctList = []
        with open(parent_dir+'/repositoryData/invertedIndexBarrels/partition_'+str(partition)+'.csv', 'r') as inverted_index_file:
            inverted_index_reader = csv.DictReader(inverted_index_file)
            for row in inverted_index_reader:
                if i == row['word_id']:
                    doctList = ast.literal_eval(row['documents'])
                    break                
        for j in doctList:
            if j in finalList:
                finalList[j] += finalList[j]+doctList[j]+20
                continue
            else:
                finalList.update({j:doctList[j]})
    
    
    if(not(broken_query == query)):
        for i in lexicon_for_broken_query:
            partition = int(i)%total_partitions
            doctList = []
            with open(parent_dir+'/repositoryData/invertedIndexBarrels/partition_'+str(partition)+'.csv', 'r') as inverted_index_file:
                inverted_index_reader = csv.DictReader(inverted_index_file)
                for row in inverted_index_reader:
                    if i == row['word_id']:
                        doctList = ast.literal_eval(row['documents'])
                        break
                        
            for j in doctList:
                if j in finalList:
                    finalList[j] += finalList[j]+doctList[j]+20
                    continue
                else:
                    finalList.update({j:doctList[j]})
    results = sorted(finalList.items(), key=lambda x: x[1], reverse=True)

    repositories = {}
    with open(parent_dir + '/repositoryData/repositories_url.csv', 'r', encoding='utf-8') as file:
    # Create a CSV reader
        csv_reader = csv.reader(file)
        
        # Read through each row in the CSV file
        for row in csv_reader:
            if len(row) >= 4:
                url = row[0]
                description = row[1]
                stars = row[2]
                forks = row[3]
                # Add the data to the dictionary
                repositories[url] = (description, stars, forks)
            else:
                print(f"Error: {row}")

    # repositories = load_important_stuff()
    final_results= []
    for doc in results:
        final_results.append((doc[0], repositories[doc[0]][0],repositories[doc[0]][1],repositories[doc[0]][2],doc[1]))
    
    return final_results  

# Main Execution
if __name__ == "__main__":

    # Input query
    query = input("Write the search query:\n")
    start_time = time.perf_counter()

    # Search documents
    final_results = search(query)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Time taken to search: {elapsed_time} seconds")
    # Output results
    # for doc in final_results:
    #     print(doc)
