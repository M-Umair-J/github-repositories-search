from flask import Flask, request, jsonify
from flask_cors import CORS
import search_algorithm  # Import the search_algorithm module
import dynamicContentAddition  # Import the dynamicContentAddition module
import os
import csv


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# def load_important_stuff():
#     # parent_dir = os.path.dirname(os.getcwd())
#     repositories = {}
#     with open(parent_dir + '/repositoryData/repositories_url.csv', 'r', encoding='utf-8') as file:
#     # Create a CSV reader
#         csv_reader = csv.reader(file)
        
#         # Read through each row in the CSV file
#         for row in csv_reader:
#             if len(row) >= 4:
#                 url = row[0]
#                 description = row[1]
#                 stars = row[2]
#                 forks = row[3]
            
#                 # Add the data to the dictionary
#                 repositories[url] = (description, stars, forks)
#     return repositories

@app.route('/api/repositories/search', methods=['GET'])
def search_repositories():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Use search_algorithm module to process the query and get results
    final_results = search_algorithm.search(query)
    results = [{"document_id": doc[0], "description": doc[1], "stars": doc[2], "forks": doc[3]} for doc in final_results[:20]]
    # Format results to return to the frontend, limiting to first 100 results
    # results
    # for i in final_results:
    #     results.append()
    # results = [{"document_id": final_results[doc][0], "description":final_results[doc][1], "stars":final_results[doc][2], "forks":final_results[doc][3]} for doc in final_results[:100]]
    # print(results)
    # results = [{"document_id": doc[0], "score": doc[1]} for doc in final_results[:100]]
    
    return jsonify(results)

@app.route('/api/repositories', methods=['GET'])
def get_repositories():
    # Placeholder for additional functionality, if required
    return jsonify([])

@app.route('/api/repositories', methods=['POST'])
def add_repository():
    # Placeholder for additional functionality, if required
    # Get data from request
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'url', 'tags']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields',
                'required': required_fields
            }), 400

        # Process repository data
        repository = {
            'title': data['title'],
            'description': data['description'],
            'url': data['url'],
            'tags': data['tags']
        }

        # Add to search index
        doc_id = dynamicContentAddition.process_new_content(repository)
        with open('repositoryData/repositories.csv', 'a') as file:
            file.write(repository['title'] + ',' + repository['description'] + ',' + repository['url'] + ',' + str(doc_id) + '\n')

        # Return success response
        return jsonify({
            'message': 'Repository added successfully',
            'repository_id': doc_id,
            'repository': repository
        }), 201

    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to add repository'
        }), 500
    # return jsonify({"message": "Repository added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
