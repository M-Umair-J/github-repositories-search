import csv
import os
import nltk
import string
import pandas as pd
from collections import defaultdict


current_dir = os.getcwd()  
parent_dir = os.path.dirname(current_dir) 

repositories_data_file = parent_dir+"/repositoryData/repositories.csv"
repositories_url_file = open(parent_dir+'/repositoryData/repositories_url.csv','w',encoding = 'utf-8')

field_names = ['url', 'description', 'stars', 'forks']

# Open the CSV file for writing with proper CSV formatting
with open(repositories_data_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    # Use csv.writer to handle CSV formatting automatically
    writer = csv.writer(repositories_url_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Write the header row
    writer.writerow([field_names[0], field_names[1], field_names[2], field_names[3]])

    # Process each row
    for i in reader:
        # Write each row of data, ensuring that fields containing commas or newlines are properly quoted
        writer.writerow([i['URL'], i['Description'], i['Stars'], i['Forks']])

# Close the file after writing
repositories_url_file.close()