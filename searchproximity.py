
Here's a simple example of implementing proximity search using Python and regular expressions:

Example: Proximity Search with Regex
python
Copy code
import re

def proximity_search(text, term1, term2, max_distance=5):
    # Create a regular expression to match the two terms within the max distance
    pattern = rf'\b(?:\S+\s+){0,max_distance}\b{re.escape(term1)}\b(?:\S+\s+){0,max_distance}\b{re.escape(term2)}\b'
    
    # Search for the pattern in the provided text
    matches = re.findall(pattern, text)
    
    return matches

# Sample text
text = "This is an example where the term1 is close to term2. And here term1 and term2 are near too."

# Search for terms within a distance of 3 words
result = proximity_search(text, 'term1', 'term2', max_distance=3)
print(result)