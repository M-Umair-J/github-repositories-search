from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for repositories
repositories = []

# Route to get all repositories
@app.route('/api/repositories', methods=['GET'])
def get_repositories():
    return jsonify(repositories)

# Route to add a new repository
@app.route('/api/repositories', methods=['POST'])
def add_repository():
    data = request.json
    title = data['title']
    description = data['description']
    url = data['url']
    tags = data['tags']
    
    # Check if tags is a string or already a list
    if isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(',')]  # Split if it's a string
    elif isinstance(tags, list):
        tags = [tag.strip() for tag in tags]  # Just strip the elements if it's already a list

    new_repository = {
        'id': str(uuid.uuid4()),  # Generate a unique ID
        'title': title,
        'description': description,
        'url': url,
        'tags': tags,
        'stars': 0,  # Initial star count
        'forks': 0,  # Initial fork count
        'createdAt': datetime.datetime.now().isoformat(),  # Add timestamp
    }

    repositories.append(new_repository)
    return jsonify(new_repository), 201  # Return newly added repository with 201 status

# Route to search repositories by title, description, or tags
@app.route('/api/repositories/search', methods=['GET'])
def search_repositories():
    query = request.args.get('query', '').lower()
    
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Search logic to match title, description, or tags
    filtered_repositories = []
    for repo in repositories:
        # Check if query matches in title or description
        if query in repo['title'].lower() or query in repo['description'].lower():
            filtered_repositories.append(repo)
        else:
            # Also search within tags
            for tag in repo['tags']:
                if query in tag.lower():
                    filtered_repositories.append(repo)
                    break

    return jsonify(filtered_repositories)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run the app on port 5000
