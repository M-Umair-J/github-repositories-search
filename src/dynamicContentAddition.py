import csv
import os
import nltk
from config import config
import string
import pandas as pd
from collections import defaultdict
from nltk.tokenize import word_tokenize
import ast
from urllib.parse import urlparse 
from math import log
from nltk.stem import WordNetLemmatizer
current_dir = os.getcwd() # getting the current working directory
parent_dir = os.path.dirname(current_dir) # using the current working directory to get the parent directory

lemmatizer = WordNetLemmatizer()
stop_words = set(nltk.corpus.stopwords.words('english'))

def tf_idf(term_freq,tot_terms,doc_freq,doc_count):
    tf = term_freq/tot_terms
    idf = log(doc_count/(1+doc_freq))
    return tf*idf

def process_new_content(repository):
    
    new_words = process_for_lexicon(repository, parent_dir)
    
    
    doc_url = add_to_filtered_repositories(repository, parent_dir)
    
    
    update_forward_index(repository, new_words, doc_url, parent_dir)
    
    
    update_inverted_index()
    update_barrels_for_lexicon()
    update_barrels_for_forward_index()
    update_barrels_for_inverted_index()
    
    with open("barrelsForForwardIndex") as f:
        code = f.read()
        exec(code)
    
    with open("barrelsForInvertedIndex") as f:
        code = f.read()
        exec(code)

    
    return doc_url

def process_for_lexicon(repository, parent_dir):
    
    # Combine all text
    all_text = f"{repository['description']} {' '.join(repository['tags'])}"
    title = repository['title']
    # Clean text
    for char in "[]',":
        all_text = all_text.replace(char, '')
    
    # Process tokens
    tokens = word_tokenize(all_text)
    filtered_words = []
    
    for token in tokens:
        token = token.lower()
        if token not in stop_words:
            lemmatized = lemmatizer.lemmatize(token)
            if not (lemmatized.isdigit() or 
                   all(char in string.punctuation for char in lemmatized) or 
                   len(lemmatized) < 3):
                filtered_words.append(lemmatized)
    filtered_words.append(title.lower())
    # Get unique words
    unique_words = set(filtered_words)
    
    # Update lexicon
    lexicon_path = f"{parent_dir}/repositoryData/lexicon.csv"
    existing_words = {}
    last_id = 0
    
    # Read existing lexicon
    with open(lexicon_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_words[row['word']] = row['id']
            last_id = max(last_id, int(row['id']))
    
    # Add new words
    new_words = {}
    with open(lexicon_path, 'a', newline='') as f:
        writer = csv.writer(f)
        for word in unique_words:
            if word not in existing_words:
                last_id += 1
                writer.writerow([last_id, word])
                new_words[word] = last_id
            else:
                new_words[word] = existing_words[word]
    
    return new_words


      

def add_to_filtered_repositories(repository, parent_dir):
    filtered_path = f"{parent_dir}/repositoryData/filtered_repositories.csv"
    
    # Process description
    description = repository['description']
    remove_characters = "[]',"
    for char in remove_characters:
        description = description.replace(char, '')
    
    desc_tokens = word_tokenize(description)
    filtered_desc_list = []
    for token in desc_tokens:
        token = token.lower()
        if token not in stop_words:
            lemmatized = lemmatizer.lemmatize(token)
            if not lemmatized.isdigit() and not all(char in string.punctuation for char in lemmatized) and len(lemmatized) >= 3:
                filtered_desc_list.append(lemmatized)
    
    # Process tags
    tags = ' '.join(repository['tags'])
    for char in remove_characters:
        tags = tags.replace(char, '')
    
    tag_tokens = word_tokenize(tags)
    filtered_tags_list = []
    for token in tag_tokens:
        token = token.lower()
        if token not in stop_words:
            filtered_tags_list.append(lemmatizer.lemmatize(token))
    
    # Create row dictionary
    new_row = {
        'url': f'"{repository["url"].strip()}"',
        'title': repository['title'].lower(),
        'data': ' '.join(filtered_desc_list),
        'tags': ' '.join(filtered_tags_list)
    }
    
    # Write to CSV
    with open(filtered_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'title', 'data', 'tags'])
        writer.writerow(new_row)
    
    return repository['url']

def update_forward_index(repository, word_ids, doc_url, parent_dir):
    forward_index_path = f"{parent_dir}/repositoryData/forward_index.csv"
    word_positions = []
    
    # Process title
    title = repository['title'].lower()
    if title in word_ids:
        word_positions.append({word_ids[title]: 't'})
    
    # Process description tokens
    desc_tokens = word_tokenize(repository['description'].lower())
    for pos, token in enumerate(desc_tokens):
        lemmatized = lemmatizer.lemmatize(token)
        if lemmatized in word_ids:
            word_positions.append({word_ids[lemmatized]: pos})
    
    # Process tags
    for tag in repository['tags']:
        lemmatized = lemmatizer.lemmatize(tag.lower())
        if lemmatized in word_ids:
            word_positions.append({word_ids[lemmatized]: 'i'})
    
    # Write to forward index
    with open(forward_index_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([doc_url, str(word_positions)])

def update_inverted_index():

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
            try:
                doc_id = row['docId'].strip()
                words_data = row['words'].strip()
                doc_id_2 = doc_id
                
                # Use ast.literal_eval instead of json.loads
                words = ast.literal_eval(words_data)
                
                for w in words:
                    if list(w.values())[0] == 't':
                        term_frequency[doc_id][list(w.keys())[0]] += 5
                    elif list(w.values())[0] == 'i':
                        term_frequency[doc_id][list(w.keys())[0]] += 2
                    else:
                        term_frequency[doc_id][list(w.keys())[0]] += 1
                    document_frequency[list(w.keys())[0]] += 1
                
                parsed_rows.append({'docId': doc_id, 'words': words})
                
            except Exception as e:
                print(f"Error processing row {i}: {str(e)}")
                print(f"Problematic data: {words_data}")
                continue
            i += 1



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
                

    # Convert word_ids to integers for sorting
    inverted_index = {int(k): v for k, v in inverted_index.items()}
    sorted_inverted_index = {str(k): inverted_index[k] for k in sorted(inverted_index)}

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


def update_barrels_for_lexicon():

    # creating barrels for lexicon
    A_to_D = {}
    E_to_H = {}
    I_to_L = {}
    M_to_P = {}
    Q_to_T = {}
    U_to_X = {}
    Y_to_Z = {}
    other = {}

    # creating a mapping of barrels and their names
    barrel_names = {'A_to_D':A_to_D,'E_to_H':E_to_H,'I_to_L':I_to_L,'M_to_P':M_to_P,'Q_to_T':Q_to_T,'U_to_X':U_to_X,'Y_to_Z':Y_to_Z,'Other':other}

    # reading lexicon file and creating barrels
    with open(parent_dir + '/repositoryData/lexicon.csv', 'r') as lexicon_file:
        reader = csv.DictReader(lexicon_file)
        for row in reader:
            w = row['word'].lower()
            # writting words to corresponding barrels
            if w: # if word is not empty
                if w[0] in 'abcd':
                    A_to_D[row['id']] = row['word']
                elif w[0] in 'efgh':
                    E_to_H[row['id']] = row['word']
                elif w[0] in 'ijkl':
                    I_to_L[row['id']] = row['word']
                elif w[0] in 'mnop':
                    M_to_P[row['id']] = row['word']
                elif w[0] in 'qrst':
                    Q_to_T[row['id']] = row['word']
                elif w[0] in 'uvwx':
                    U_to_X[row['id']] = row['word']
                elif w[0] in 'yz':
                    Y_to_Z[row['id']] = row['word']
                else:
                    other[row['id']] = row['word']
        
    # creating lexicon barrels directory
    lexicon_barrels_dir = parent_dir+"/repositoryData/lexicon_barrels/"
    # ensure directories exist
    os.makedirs(lexicon_barrels_dir, exist_ok=True)

    # writting to barrels
    for barrel in barrel_names:
        with open(lexicon_barrels_dir + barrel + '.csv', 'w') as lexicon_barrel:
            writer = csv.DictWriter(lexicon_barrel, fieldnames=['id', 'words'])
            writer.writeheader()
            for word in barrel_names[barrel]:
                writer.writerow({'id': word, 'words': barrel_names[barrel][word]})    
            

def update_barrels_for_forward_index():
    # creating barrels for forward_index
    A_to_D = {}
    E_to_H = {}
    I_to_L = {}
    M_to_P = {}
    Q_to_T = {}
    U_to_X = {}
    Y_to_Z = {}
    other = {}

    # creating a mapping of barrels and their names
    barrel_names = {'A_to_D':A_to_D,'E_to_H':E_to_H,'I_to_L':I_to_L,'M_to_P':M_to_P,'Q_to_T':Q_to_T,'U_to_X':U_to_X,'Y_to_Z':Y_to_Z,'Other':other}

    with open(parent_dir + '/repositoryData/forward_index.csv', 'r') as forward_index:
        reader = csv.DictReader(forward_index)
        for row in reader:
            url = row['docId'].lower()
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip("/").split("/")  # split path and remove leading/trailing slashes
            if (len(path_parts)==2):
                repositoryName = path_parts[1]
            else:
                print("invalid")
            # writting words to corresponding barrels
            if repositoryName: # if word is not empty
                if repositoryName[0] in 'abcd':
                    A_to_D[row['docId']] = row['words']
                elif repositoryName[0] in 'efgh':
                    E_to_H[row['docId']] = row['words']
                elif repositoryName[0] in 'ijkl':
                    I_to_L[row['docId']] = row['words']
                elif repositoryName[0] in 'mnop':
                    M_to_P[row['docId']] = row['words']
                elif repositoryName[0] in 'qrst':
                    Q_to_T[row['docId']] = row['words']
                elif repositoryName[0] in 'uvwx':
                    U_to_X[row['docId']] = row['words']
                elif repositoryName[0] in 'yz':
                    Y_to_Z[row['docId']] = row['words']
                else:
                    other[row['docId']] = row['words']

    # creating forward_index barrels directory
    forward_index_barrels_dir = parent_dir+"/repositoryData/forward_index_barrels/"
    # ensure directories exist
    os.makedirs(forward_index_barrels_dir, exist_ok=True)

    # writting to barrels
    for barrel in barrel_names:
        with open(forward_index_barrels_dir + barrel + '.csv', 'w') as lexicon_barrel:
            writer = csv.DictWriter(lexicon_barrel, fieldnames=['docId', 'words'])
            writer.writeheader()
            for docId in barrel_names[barrel]:
                writer.writerow({'docId': docId, 'words': barrel_names[barrel][docId]})

def update_barrels_for_inverted_index():
    # Load the inverted index CSV file
    inverted_index_df = pd.read_csv(parent_dir+'/repositoryData/inverted_index.csv')

    # Define the size of each partition (bucket size)

    partition_size = 10000
    total_word_ids = len(inverted_index_df)  # Total number of word IDs
    total_partitions = total_word_ids // partition_size + (1 if total_word_ids % partition_size != 0 else 0)  # Total partitions

    config.update_total_partitions(total_partitions)  # Update the total partitions in the config file

    # Add a column for partition number based on word_id or row index
    inverted_index_df['partition'] = inverted_index_df['word_id'] % total_partitions

    # Create a relative path for the output folder
    output_dir = parent_dir+'/repositoryData/invertedIndexBarrels'  # Relative path for the partitions folder
    os.makedirs(output_dir, exist_ok=True)  # Create the folder if it doesn't exist

    # Group the dataframe by partition number and save each group to a separate file
    for partition_number, partition_df in inverted_index_df.groupby('partition'):
        # Define the file name for each partition
        output_file = os.path.join(output_dir, f'partition_{partition_number}.csv')
        
        # Save the partition to a separate file
        partition_df.to_csv(output_file, index=False)