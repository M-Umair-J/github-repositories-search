import pandas as pd
import os
from config import config

current_dir = os.getcwd() # getting the current working directory
parent_dir = os.path.dirname(current_dir) # using the current working directory to get the parent directory

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