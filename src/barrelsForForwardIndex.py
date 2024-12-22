import os
import csv
from urllib.parse import urlparse # for extracting the repository name from the URL

current_dir = os.getcwd() # getting the current working directory
parent_dir = os.path.dirname(current_dir) # using the current working directory to get the parent directory

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
barrel_names = {'A_to_D':A_to_D,'E to H':E_to_H,'I to L':I_to_L,'M to P':M_to_P,'Q to T':Q_to_T,'U to X':U_to_X,'Y to Z':Y_to_Z,'Other':other}

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
