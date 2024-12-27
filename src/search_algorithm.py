import nltk
import os
import csv
from config import config
import ast
import sys

# Configuration
total_partitions = config.get_total_partitions()

# Increase CSV field size limit to handle large files
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / 10)

# Paths
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)

# Initialize Lemmatizer
lemmatizer = nltk.WordNetLemmatizer()

# Characters to replace in the query
characters_of_interest = ['/', ',', '.', '-', '_']

def load_lexicon_files():
    """Pre-load all lexicon files into memory."""
    lexicon_data = {}
    barrels = [
        ('A_to_D.csv', 'abcd'),
        ('E_to_H.csv', 'efgh'),
        ('I_to_L.csv', 'ijkl'),
        ('M_to_P.csv', 'mnop'),
        ('Q_to_T.csv', 'qrst'),
        ('U_to_X.csv', 'uvwx'),
        ('Y_to_Z.csv', 'yz'),
        ('Other.csv', '')
    ]

    for file_name, letters in barrels:
        file_path = os.path.join(parent_dir, 'repositoryData', 'lexicon_barrels', file_name)
        with open(file_path, 'r', encoding='utf-8') as lex_file:
            reader = csv.DictReader(lex_file)
            for row in reader:
                first_letter = row['words'][0].lower() if row['words'] else ''
                if not letters or first_letter in letters:
                    lexicon_data[row['words'].lower()] = row

    return lexicon_data

def find_the_word_ids(query_list, lexicon_data):
    """Find word IDs from pre-loaded lexicon data."""
    lexicon = {}
    lexicon_word_to_id = {}
    
    for word in query_list:
        word = word.lower()
        if word in lexicon_data:
            entry = lexicon_data[word]
            lexicon[entry['id']] = entry['words']
            lexicon_word_to_id[entry['words']] = entry['id']

    return lexicon, lexicon_word_to_id

def search_documents(lexicon):
    """Search documents using word IDs in the inverted index."""
    final_list = []
    for word_id in lexicon:
        partition = int(word_id) % total_partitions
        file_path = os.path.join(parent_dir, 'repositoryData', 'invertedIndexBarrels', f'partition_{partition}.csv')

        with open(file_path, 'r', encoding='utf-8') as inverted_index_file:
            reader = csv.DictReader(inverted_index_file)
            for row in reader:
                if word_id == row['word_id']:
                    doc_list = ast.literal_eval(row['documents'])
                    sorted_docs = sorted(doc_list.items(), key=lambda x: x[1], reverse=True)
                    final_list.extend(sorted_docs)
                    break

    return final_list

def process_query(query):
    """Process and lemmatize the input query."""
    for char in characters_of_interest:
        query = query.replace(char, ' ')
    
    tokens = nltk.word_tokenize(query)
    lemmatized_query = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    return lemmatized_query

# Main Execution
if __name__ == "__main__":
    # Preload lexicon files
    lexicon_data = load_lexicon_files()

    # Input query
    query = input("Write the search query:\n")
    query_list = process_query(query)

    # Find word IDs
    lexicon, lexicon_word_to_id = find_the_word_ids(query_list, lexicon_data)

    # Search documents
    final_results = search_documents(lexicon)

    # Output results
    for doc in final_results:
        print(doc[0])
