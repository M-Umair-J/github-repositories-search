mport csv
import os
import nltk

import string

current_dir = os.getcwd()  
parent_dir = os.path.dirname(current_dir)  


filtered_repositories_file = parent_dir + '/repositoryData/filtered_repositories.csv'
lexicon_file = parent_dir + '/repositoryData/lexicon.csv'
inverted_index_file = parent_dir + '/repositoryData/inverted_index.csv'


lexicon = {}
with open(lexicon_file, 'r', encoding='utf-8') as lex:
    reader = csv.DictReader(lex)
    for row in reader:
        lexicon[row['word']] = row['id']  


inverted_index = {}


with open(filtered_repositories_file, 'r', encoding='utf-8') as filtered:
    reader = csv.DictReader(filtered)
    for row in reader:
        document_id = row['url']  
        document = row['data']  
       
        document = nltk.word_tokenize(document)
        
       
        for word in document:
            if word in lexicon:  # Ensure the word is in the lexicon
                word_id = lexicon[word]  
                
                
                if word_id not in inverted_index:
                    inverted_index[word_id] = []  # Initialize a list for new word ID
                
                if document_id not in inverted_index[word_id]:  
                    inverted_index[word_id].append(document_id)


with open(inverted_index_file, 'w', encoding='utf-8') as inverted_file:
    writer = csv.writer(inverted_file)
    writer.writerow(['word_id', 'document_ids'])  
    
    for word_id, document_ids in inverted_index.items():
        document_ids_str = " ".join(document_ids)  
        writer.writerow([word_id, document_ids_str])
