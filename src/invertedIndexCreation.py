import csv
import os
import json

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


inverted_index = {}
# loading forward index and parsing it to create list of json objects
parsed_rows = []
with open(forward_index, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        doc_id = row['docId'].strip()
        words_data = row['words'].strip()

        words_data = words_data.replace("'", '"') # replacing single quotes with double quotes to make it valid json

        # convert the words string into a JSON object
        words = json.loads(words_data)
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
        key = list(key.keys())[0]
        if key not in inverted_index:
            inverted_index[key] = []
        if document_id not in inverted_index[key]:
            inverted_index[key].append(document_id)

# writing inverted index to a csv file
with open(inverted_index_file, 'w', encoding='utf-8') as inverted_file:
    writer = csv.writer(inverted_file)
    writer.writerow(['word_id', 'documents'])  
    for word_id, documents in inverted_index.items():
        writer.writerow([word_id, documents])
