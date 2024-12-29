import csv
import os
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(nltk.corpus.stopwords.words('english'))

def process_new_content(repository):
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    
    # Step 1: Process and add to lexicon
    new_words = process_for_lexicon(repository, parent_dir)
    
    # Step 2: Add to filtered repositories
    doc_url = add_to_filtered_repositories(repository, parent_dir)
    
    # Step 3: Update forward index
    update_forward_index(repository, new_words, doc_url, parent_dir)
    
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
