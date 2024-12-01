import csv
import os
import nltk
import string
import pandas as pd


current_dir = os.getcwd()  
parent_dir = os.path.dirname(current_dir) 

repositories_data_titles = []
repositories_data = []
repositories_data_file = parent_dir+"/repositoryData/repositories.csv"
filtered_repositories_file = open(parent_dir+'/repositoryData/filtered_repositories.csv','w',encoding = 'utf-8')
stop_words = set(nltk.corpus.stopwords.words('english')) 
lemmatizer = nltk.WordNetLemmatizer()


#creating the filtered repositories data set with relevant fields only
with open(repositories_data_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    # headers = next(reader)
    # rows = [row for row in reader]  
    field_names = ['url','title','data','tags']
    filtered_repositories_file.write(field_names[0]+","+field_names[1]+","+field_names[2]+","+field_names[1]+"\n")
    for i in reader:
        strf = i['Description']
        strf2 = i['Topics']
        remove_characters = "[]',"
        for j in remove_characters:
            strf = strf.replace(j, '')
            strf2 = strf2.replace(j, '')
        strf = nltk.word_tokenize(strf)
        strf2 = nltk.word_tokenize(strf2)
        filtered_data_list = []
        filtered_tags_list = []
        for k in strf:
            k = k.lower()
            if k.casefold() not in stop_words:
                filtered_data_list.append(lemmatizer.lemmatize(k))
        for k in strf2:
            k = k.lower()
            if k.casefold() not in stop_words:
                filtered_tags_list.append(lemmatizer.lemmatize(k))

        data_list = []
        for l in filtered_data_list:
            if not ("".join(l).strip()).isdigit() and not all(char in string.punctuation for char in l) and not len(l)<3:
                data_list.append(l)
        data_list = " ".join(data_list)
        filtered_tags_list = " ".join(filtered_tags_list)
        data_list = f"\"{i['URL']}\""+","+i['Name'].lower()+","+data_list+","+filtered_tags_list
        filtered_repositories_file.write(data_list+"\n")


forward_index = {} # creating the dictionary for forward index to store key value pairs of docId and word ids
lexicon = {} # creating the dictionary for lexicon to store key value pairs of words and their ids (loaded from the lexicon file)
with open(parent_dir+'/repositoryData/lexicon.csv', 'r', encoding='utf-8') as lex:
    reader = csv.DictReader(lex)
    for row in reader:
        lexicon[row['word']] = row['id'] # mapping words to their ids in dictionary

with open(parent_dir+'/repositoryData/filtered_repositories.csv', 'r', encoding='utf-8') as filtered:
    reader = csv.reader(filtered)
    header = next(reader)
    for row in reader:
        document = nltk.word_tokenize(row[2])
        title = row[1]
        tags = nltk.word_tokenize(row[3])
        
        word_ids_with_positions = []
        id_position_pairs = {} # creating mapping for words and their respective postions in the document

        if title in lexicon:
            id_position_pairs[lexicon[title]] = 't' # since (repositories have a single word title so we are using 't' to represent title position which will be later used for better weightage calculation)
            word_ids_with_positions.append(id_position_pairs)
        for position,word in enumerate(document):
            if word in lexicon:
                id_position_pairs={}
                id_position_pairs[lexicon[word]] = position
                word_ids_with_positions.append(id_position_pairs)
        for word in tags:
            if word in lexicon:
                id_position_pairs={}
                id_position_pairs[lexicon[word]] = 'i' # since the position of the words in tags don't matter in the context searching so we are using 'i' to represent that the position is irrelevant if the word appears in the tags
                word_ids_with_positions.append(id_position_pairs)
        forward_index[row[0]] = word_ids_with_positions # mapping documents to their respective word ids and their positions
        

# writting the forward index to a csv file
with open(parent_dir+'/repositoryData/forward_index.csv','w',encoding = 'utf-8') as forward: 
    writer = csv.writer(forward)
    writer.writerow(['docId','words'])
    for docId,words in forward_index.items():
        writer.writerow([docId,words])

