import csv
import os
import nltk
import string
import pandas as pd

# Ensure necessary NLTK data is downloaded
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# def remove_duplicates_from_list(l):
#     return list(dict.fromkeys(l))


current_dir = os.getcwd()  # getting the current working directory
parent_dir = os.path.dirname(current_dir)  # using the current working directory to get the parent directory

repositories_data_titles = []
repositories_data = []
repositories_data_file = parent_dir+"/repositoryData/repositories.csv"
filtered_repositories_file = open(parent_dir+'/repositoryData/filtered_repositories.csv','w',encoding = 'utf-8')
stop_words = set(nltk.corpus.stopwords.words('english')) 
lemmatizer = nltk.WordNetLemmatizer()

with open(repositories_data_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Read the header row first
    rows = [row for row in reader]  # Read the rest of the rows into 'rows' variable
    field_names = ['url','data']
    filtered_repositories_file.write(field_names[0]+","+field_names[1]+"\n")
    for i in rows:
        strf = i[1]+" "+i[13]
        
        remove_characters = "[]',"
        for j in remove_characters:
            strf = strf.replace(j, '')
        strf = nltk.word_tokenize(strf)
        filtered_data_list = []
        for k in strf:
            k = k.lower()
            if k.casefold() not in stop_words:
                filtered_data_list.append(lemmatizer.lemmatize(k))
                data_list = []
        for l in filtered_data_list:
            if not ("".join(l).strip()).isdigit() and not all(char in string.punctuation for char in l) and not len(l)<3:
                data_list.append(l)
        data_list = " ".join(data_list)
        data_list = f"\"{i[2]}\""+","+i[0]+" "+data_list
        filtered_repositories_file.write(data_list+"\n")


forward_index = {}
lexicon = {}
with open(parent_dir+'/repositoryData/lexicon.csv', 'r', encoding='utf-8') as lex:
    reader = csv.DictReader(lex)
    for row in reader:
        lexicon[row['word']] = row['id']

with open(parent_dir+'/repositoryData/filtered_repositories.csv', 'r', encoding='utf-8') as filtered:

    reader = csv.DictReader(filtered)
    for row in reader:
        document_id = row['url']
        document = row['data']
        document = nltk.word_tokenize(document)
        word_ids = []
        for position, word in enumerate(document):
            if word in lexicon:
                word_ids.append(lexicon[word])
        forward_index[document_id] = word_ids

with open(parent_dir+'/repositoryData/forward_index.csv', 'w', encoding='utf-8') as forward:
    writer = csv.writer(forward)
    writer.writerow(['document_id', 'words_ids'])
    for document_id, words_ids in forward_index.items():
        document_id = "".join(document_id)
        document_id = f"{document_id}"
        word_ids = " ".join(words_ids)
        writer.writerow([document_id, word_ids])