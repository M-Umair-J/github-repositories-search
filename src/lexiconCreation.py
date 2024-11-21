
import csv
import os
import nltk
import re # for regular expressions to filter out the unnecessary punctuations


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
    repositories_data_titles.append(f"##{i[0]}##")
    repositories_data.append(i[1])
    repositories_data.append(i[13])

repositories_data = remove_duplicates_from_list(repositories_data)
repositories_data_titles = remove_duplicates_from_list(repositories_data_titles)
repositories_data = " ".join(repositories_data)
repositories_data_titles = " ".join(repositories_data_titles)
