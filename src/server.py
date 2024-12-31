from flask import Flask, request, jsonify
from flask_cors import CORS
import search_algorithm  # Import the search_algorithm module
import dynamicContentAddition  # Import the dynamicContentAddition module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Pre-load the lexicon once at the server start

@app.route('/api/repositories/search', methods=['GET'])
def search_repositories():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Use search_algorithm module to process the query and get results
    final_results = search_algorithm.search(query)

    # Format results to return to the frontend, limiting to first 100 results
    results = [{"document_id": doc[0], "score": doc[1]} for doc in final_results[:100]]
    
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
