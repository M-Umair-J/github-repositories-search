# GitHub Repository Search Engine

## Introduction

This project implements a search engine for GitHub repositories, allowing users to search, index, and rank repositories based on keywords. The search engine is built with a Python backend and a React-based frontend. It uses a custom indexing system to efficiently retrieve and rank relevant GitHub repositories based on user queries. The goal of this project is to create a scalable and responsive search engine that can handle large datasets, using techniques such as lexicons, forward and inverted indexes, and dynamic content addition.

## Key Components

1. **Lexicon**: 
   - The lexicon stores all unique words found in the dataset (GitHub repositories). Each word is assigned a unique index, allowing for easy reference during the indexing and search process.

2. **Forward Index**: 
   - The forward index maps each word to the documents (repositories) in which it appears. This helps in the creation of the inverted index, which will be used for the actual search query processing.

3. **Inverted Index**: 
   - The inverted index maps words to the list of repositories that contain them. This allows the system to quickly find relevant repositories for any search query, as it stores the relationships between words and repositories.

4. **Barrel Implementation**:
   - The inverted index is divided into smaller chunks called barrels. Barrels help in efficiently managing memory, especially when dealing with large datasets. By breaking the index into manageable sections, the search engine can handle large-scale datasets without overwhelming system memory.

## Ranking Criteria

The ranking of the repositories is determined based on several factors:

- **Stars**: 
   - The more stars a repository has, the more popular it is considered. Repositories with higher star counts are ranked higher.
   
- **Forks**: 
   - Fork count indicates how many times a repository has been copied and modified by other users. A higher number of forks implies more widespread usage and is considered an indicator of quality.
   
- **Matches of Words**: 
   - Repositories that contain a higher number of exact word matches to the search query will rank higher. This takes into account both the number of occurrences of the search words and their placement within the repository’s description or content.
   
- **Discussions**: 
   - Repositories with active discussions or more interaction around issues, pull requests, and comments tend to be ranked higher. Engagement within the community is a sign of relevance and importance.

## Features

- **Lexicon**: Stores all unique words from the GitHub repository dataset with distinct indices.
- **Forward Index**: Maps words to the documents (repositories) they appear in, facilitating the creation of the inverted index.
- **Inverted Index**: Maps words to the list of repositories that contain them, which is used during searches.
- **Single Word Search**: Allows users to search for repositories based on a single keyword.
- **Multi-Word Search**: Supports search queries with multiple keywords, returning results where all words are present in any order.
- **Ranking**: Results are ranked based on keyword frequency and document relevance.
- **Barrels**: Inverted index is divided into smaller chunks (barrels) for improved memory management and scalability.
- **Dynamic Content Addition**: Allows new repositories to be indexed automatically and appear in search results.
- **System Scalability**: Optimized to handle datasets with a large number of GitHub repositories with minimal slowdown.
- **Web Interface**: A React-based UI to enter search queries, view results, and add new repositories.

## Technologies Used

- **Backend**: Python (Flask for API)
- **Frontend**: React.js
- **Data Source**: [GitHub repositories dataset](https://www.kaggle.com/datasets/donbarbos/github-repos)
- **Storage**: File-based indexing (no databases used)

