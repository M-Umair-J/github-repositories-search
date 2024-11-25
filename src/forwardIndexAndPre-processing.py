import csv
import os
import nltk
import string

# Ensure necessary NLTK data is downloaded
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# def remove_duplicates_from_list(l):
#     return list(dict.fromkeys(l))


# current_dir = os.getcwd()  # getting the current working directory
# parent_dir = os.path.dirname(current_dir)  # using the current working directory to get the parent directory

# repositories_data_titles = []
# repositories_data = []
# repositories_data_file = "C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/repositories.csv"
# lexicon = open('C:\\Users\\Saim Tariq\\Desktop\\DSA project\\github-repositories-search\\repositoryData\\filtered_repositories.csv','w',encoding = 'utf-8')
# stop_words = set(nltk.corpus.stopwords.words('english'))  # getting common english stopwords
# lemmatizer = nltk.WordNetLemmatizer()  # creating a lemmatizer for converting tokens into their base forms
# # Reading from the repositories file using csv reader
# # Filtering the name, title, and topics fields
# with open(repositories_data_file, 'r', encoding='utf-8') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read the header row first
#     rows = [row for row in reader]  # Read the rest of the rows into 'rows' variable
#     for i in rows:
#         strf = i[0]+" "+i[1]+" "+i[13]
        
#         remove_characters = "[]',"
#         for i in remove_characters:
#             strf = strf.replace(i, '')
#         strf = nltk.word_tokenize(strf)
#         filtered_data_list = []
#         for i in strf:
#             i = i.lower()
#             if i.casefold() not in stop_words:  # filtering out the stopwords in the data
#                 filtered_data_list.append(lemmatizer.lemmatize(i))
#         filtered_data_list = " ".join(filtered_data_list)
#         lexicon.write(filtered_data_list+"\n")

# import pandas as pd

# lexicons_df = pd.read_csv("C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/lexicon.csv")
# dataset_df = pd.read_csv("C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/filtered_repositories.csv")

#for creating id and words in csv file to easily access
# # Initialize empty lists to hold the data
# ids = []
# words = []
# i = 0
# # Read the CSV file line by line
# with open('C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/lexicon.csv', 'r', encoding='utf-8') as file:
#     for line in file:
       
#         # Split the line into ID and word based on the space separating them
#         parts = line.strip().split(' ', 1)  # Split into two parts: ID and word
#         if len(parts) == 2:
#             ids.append(parts[0])   # The ID (number)
#             words.append(parts[1])  # The word

# # Now you can create a DataFrame
# lexicons_df = pd.DataFrame({
#     'id': ids,
#     'words': words
# })

# output_file = 'C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/lexicons_output.csv'
# lexicons_df.to_csv(output_file, index=False, encoding='utf-8')  # index=False to avoid writing row indices








#for creating document id and document as a column

# df = pd.read_csv('C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/filtered_repositories.csv', 
#                  header=None, 
#                  names=['document'], 
#                  dtype={0: str})
# # Assign a unique document ID starting from 1
# df['document_id'] = range(1, len(df) + 1)

# # Reorder the columns so that 'document_id' is first and 'document' is second
# df = df[['document_id', 'document']]

# # Save the updated DataFrame to a new CSV file
# df.to_csv('C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/documents_with_ids.csv', index=False)





import pandas as pd

# Load the lexicons and dataset
lexicons_df = pd.read_csv('C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/lexicons_output.csv')
dataset_df = pd.read_csv('C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/documents_with_ids.csv')

# Create a map of lexicon words to their corresponding lexicon ids
lexicon_map = {row['words']: row['id'] for _, row in lexicons_df.iterrows()}

# Initialize the forward index to store document_id and corresponding lexicon_ids
forward_index = {}

# Iterate through each row in the dataset
for _, row in dataset_df.iterrows():
    document_id = row['document_id']  # Get the document ID
    document = row['document']  # Get the document content
    
    # Split the document into individual words (if document is a string)
    tokens = document.split() if isinstance(document, str) else document
    
    # Find matching lexicon IDs in the document
    matching_ids = [lexicon_map[token] for token in tokens if token.lower() in lexicon_map]  # Check if token exists in lexicon_map
    
    # If there are matching lexicon IDs, save them in the forward_index
    if matching_ids:
        forward_index[document_id] = matching_ids

# Print the forward index to verify the result
forward_index_df = pd.DataFrame(list(forward_index.items()), columns=['document_id', 'lexicon_ids'])

# Save the DataFrame to a CSV file
forward_index_df.to_csv('C:/Users/Saim Tariq/Desktop/DSA project/github-repositories-search/repositoryData/forward_index.csv', index=False)