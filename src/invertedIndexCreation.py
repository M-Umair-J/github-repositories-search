import csv
import os
import json
from collections import defaultdict
from math import log

def tf_idf(term_freq,tot_terms,doc_freq,doc_count):
    tf = term_freq/tot_terms
    idf = log(doc_count/(1+doc_freq))
    return tf*idf
      
current_dir = os.getcwd()  
parent_dir = os.path.dirname(current_dir)  


forward_index = parent_dir + '/repositoryData/forward_index.csv'
lexicon_file = parent_dir + '/repositoryData/lexicon.csv'
inverted_index_file = parent_dir + '/repositoryData/inverted_index.csv'

# loading lexicon into dictionary
lexicon = {}
with open(lexicon_file, 'r', encoding='utf-8') as lex:
    reader = csv.DictReader(lex)
    for row in reader:
        lexicon[row['word']] = row['id']  


term_frequency = defaultdict(lambda: defaultdict(int))
document_frequency = defaultdict(int)

inverted_index = {}
# loading forward index and parsing it to create list of json objects
parsed_rows = []
with open(forward_index, 'r') as file:
    reader = csv.DictReader(file)
    i = 1
    for row in reader:
        doc_id = row['docId'].strip()
        words_data = row['words'].strip()
        doc_id_2 = doc_id
        words_data = words_data.replace("'", '"') # replacing single quotes with double quotes to make it valid json
        # convert the words string into a JSON object
        words = json.loads(words_data)
        
        for w in words:
            if list(w.values())[0] == 't':
                term_frequency[doc_id][list(w.keys())[0]]+=5
            elif list(w.values())[0] == 'i':
                term_frequency[doc_id][list(w.keys())[0]]+=2
            else:
                term_frequency[doc_id][list(w.keys())[0]]+=1
        words_set = set()
        for w in words:  
            words_set.add(list(w.keys())[0])
        for w in words_set:
            document_frequency[w]+=1
        
        # create a JSON object for the row
        parsed_rows.append({
            "docId": doc_id,
            "words": words
        })



# creating inverted index
for row in parsed_rows:
    document_id = row['docId']
    words = row['words']
    for key in words:
        weightage = tf_idf(term_frequency[document_id][list(key.keys())[0]],len(term_frequency[document_id]),document_frequency[list(key.keys())[0]],len(parsed_rows))
        key = list(key.keys())[0]
        if key not in inverted_index:
            inverted_index[key] = {}
        if document_id not in inverted_index[key]:
            inverted_index[key][document_id] = weightage
            

sorted_inverted_index = {k: inverted_index[k] for k in sorted(inverted_index)}
with open(inverted_index_file, 'w', encoding='utf-8') as inverted_file:
    writer = csv.writer(inverted_file)
    writer.writerow(['word_id', 'documents'])  
    for word_id, documents in sorted_inverted_index.items():
        writer.writerow([word_id, documents])

# writing inverted index to a csv file
with open(inverted_index_file, 'w', encoding='utf-8') as inverted_file:
    writer = csv.writer(inverted_file)
    writer.writerow(['word_id', 'documents'])  
    for word_id, documents in inverted_index.items():
        writer.writerow([word_id, documents])
