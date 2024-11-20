
# GitHub Repository Search Engine

## Introduction

This project implements a search engine for GitHub repositories, allowing users to search, index, and rank repositories based on keywords. The search engine is built with a Python backend and a React-based frontend. It leverages a custom indexing system to efficiently retrieve and rank relevant GitHub repositories based on user queries. The goal of this project is to create a scalable and responsive search engine that can handle large datasets, using techniques such as lexicons, forward and inverted indexes, and dynamic content addition.

## Features

- **Lexicon**: Stores all unique words from the GitHub repository dataset with distinct indices.
- **Forward Index**: Maps words to the documents (repositories) they appear in, facilitating the creation of the inverted index.
- **Inverted Index**: Maps words to the list of repositories that contain them, which is used during searches.
- **Single Word Search**: Allows users to search for repositories based on a single keyword.
- **Multi-Word Search**: Supports search queries with multiple keywords, returning results where all words are present in any order.
- **Ranking**: Results are ranked based on keyword frequency and document relevance.
- **Barrels**: Inverted index is divided into smaller chunks (barrels) for improved memory management and scalability.
- **Dynamic Content Addition**: Allows new repositories to be indexed automatically and appear in search results.
- **System Scalability**: Optimized to handle datasets with over 45,000 GitHub repositories with minimal slowdown.
- **Web Interface**: A React-based UI to enter search queries, view results, and add new repositories.

## Technologies Used

- **Backend**: Python (Flask or Django for API)
- **Frontend**: React.js
- **Data Source**: GitHub repositories dataset
- **Storage**: File-based indexing (no databases used)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
