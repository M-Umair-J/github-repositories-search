import os
import csv


current_dir = os.getcwd() # getting the current working directory
parent_dir = os.path.dirname(current_dir) # using the current working directory to get the parent directory


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
barrel_names = {'A_to_D':A_to_D,'E to H':E_to_H,'I to L':I_to_L,'M to P':M_to_P,'Q to T':Q_to_T,'U to X':U_to_X,'Y to Z':Y_to_Z,'Other':other}

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
        