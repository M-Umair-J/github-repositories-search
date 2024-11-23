import csv
import os
import nltk
import string

def remove_duplicates_from_list(l):
    return list(dict.fromkeys(l))


current_dir = os.getcwd() # getting the current working directory
parent_dir = os.path.dirname(current_dir) # using the current working directory to get the parent directory

# reading from the repositories file using csv reader
repositories_data_titles = [] 
repositories_data= []
repositories_data_file = open(parent_dir+'/repositoryData/repositories.csv','r')
reader = csv.reader(repositories_data_file)
# filtering the name, title and topics fields
for i in reader:
    if(i[0] == 'Name'): # skipping the first row containing the field names
        continue
    repositories_data_titles.append(f"{i[0]}")
    repositories_data.append(i[1])
    repositories_data.append(i[13])


repositories_data = " ".join(repositories_data)
repositories_data_titles = " ".join(repositories_data_titles)

#removing the unnecassary characters
remove_characters = "[]',"
for i in remove_characters:
    repositories_data = repositories_data.replace(i,'')


# tokenizing the string
repositories_data_titles = nltk.word_tokenize(repositories_data_titles)
repositories_data = nltk.word_tokenize(repositories_data)

# removing the stopwords
filtered_data_list = []
stop_words = set(nltk.corpus.stopwords.words('english')) # getting common english stopwords
for i in repositories_data:
    if i.casefold() not in stop_words: # filtereing out the stopwords in the data
        filtered_data_list.append(i)

#removing all the duplicates
filtered_data_list = remove_duplicates_from_list(filtered_data_list)
repositories_data_titles = remove_duplicates_from_list(repositories_data_titles)

# writting to lexicon file
z = 1
lexicon = open(parent_dir+'/repositoryData/lexicon.csv','a')
for i in filtered_data_list:
    if not ("".join(i).strip()).isdigit() and not all(char in string.punctuation for char in i) and not len(i)<3: # filtering out elements with pure punctuations, purely numbers or words with less then 3 characters to make sure lexicon has more meaninful words
        lexicon.write(f"{z} {i} \n")
    z+=1
lexicon = open(parent_dir+'/repositoryData/lexicon.csv','a')
for i in repositories_data_titles:
    lexicon.write(f"{z} {i} \n")
    z+=1
