import pandas as pd

# Load the inverted index CSV file
inverted_index_df = pd.read_csv('github-repositories-clone/inverted_index.csv')

# Define the size of each partition (bucket size)
partition_size = 10000
total_word_ids = len(inverted_index_df)  # Total number of word IDs
total_partitions = total_word_ids // partition_size + (1 if total_word_ids % partition_size != 0 else 0)  # Total partitions

# Open the output file to store partitioned data
with open('github-repositories-clone/partitioned_inverted_index.csv', 'w') as f:
    # Write the header for the file
    f.write('partition,word_id,documents\n')
    
    # Iterate through each row in the inverted index dataframe
    for _, row in inverted_index_df.iterrows():
        word_id = row['word_id']  # Extract the word ID
        documents = row['documents']  # Extract the associated documents
        
        # Calculate the partition number using modulo operation
        partition_number = word_id % total_partitions
        
        # Write the partition number, word_id, and associated documents to the output file
        f.write(f'{partition_number},{word_id},{documents}\n')

print(f"Partitioned data saved to 'github-repositories-clone/partitioned_inverted_index.csv'.")
