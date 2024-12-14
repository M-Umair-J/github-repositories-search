import pandas as pd
import nltk
import string
from collections import defaultdict

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the lexicon and document dataset
lexicons_df = pd.read_csv('github-repositories-clone\lexicon.csv')
dataset_df = pd.read_csv('C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/documents_with_ids.csv')

# Create a map of lexicon words to their corresponding lexicon ids
lexicon_map = {row['words']: row['id'] for _, row in lexicons_df.iterrows()}

# Initialize the forward index to store document_id and corresponding lexicon_ids
forward_index = {}

# Inverted Index (Barrel Creation)
inverted_index = defaultdict(list)  # Mapping from lexicon_id to list of document_ids

# Iterate through each document to build forward and inverted indexes
for _, row in dataset_df.iterrows():
    document_id = row['document_id']
    document = row['document']
    
    # Tokenize the document into words
    tokens = nltk.word_tokenize(document.lower())  # Convert to lower case for uniformity
    
    # Find matching lexicon IDs in the document
    for token in tokens:
        if token in lexicon_map:
            lexicon_id = lexicon_map[token]
            # Add the document ID to the inverted index for this lexicon ID
            inverted_index[lexicon_id].append(document_id)
            
            # Build the forward index (document -> list of lexicon_ids)
            if document_id not in forward_index:
                forward_index[document_id] = []
            forward_index[document_id].append(lexicon_id)

# Save the forward index to a CSV
forward_index_df = pd.DataFrame(list(forward_index.items()), columns=['document_id', 'lexicon_ids'])
forward_index_df.to_csv('C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/forward_index.csv', index=False)

# Save the inverted index (barrels) to a CSV
inverted_index_df = pd.DataFrame([(lexicon_id, document_id) for lexicon_id, doc_list in inverted_index.items() for document_id in doc_list], columns=['lexicon_id', 'document_id'])
inverted_index_df.to_csv('C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/inverted_index.csv', index=False)

