import { useState, useEffect } from 'react';
import { Github, Plus } from 'lucide-react';
import { SearchBar } from './components/SearchBar';
import { RepositoryForm } from './components/RepositoryForm';
import { Modal } from './components/Modal';
import { TrendingRepositories } from './components/TrendingRepositories';

function App() {
  const [repositories, setRepositories] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Fetch search results from the backend
  useEffect(() => {
    if (searchQuery) {
      const fetchSearchResults = async () => {
        try {
          const response = await fetch(
            `http://localhost:5000/api/repositories/search?query=${encodeURIComponent(searchQuery)}`
          );
          if (response.ok) {
            const results = await response.json();
            setSearchResults(results); // Assuming the response is an array of repositories
          } else {
            setSearchResults([]);
            console.error('Failed to fetch search results');
          }
        } catch (error) {
          console.error('Error fetching search results:', error);
          setSearchResults([]);
        }
      };
      fetchSearchResults();
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  const handleAddRepository = async (formData) => {
    const newRepository = {
      title: formData.title,
      description: formData.description,
      url: formData.url,
      tags: formData.tags.split(',').map((tag) => tag.trim()).filter(Boolean),
    };

    const response = await fetch('http://localhost:5000/api/repositories', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newRepository),
    });

    if (response.ok) {
      const addedRepository = await response.json();
      setRepositories([addedRepository, ...repositories]);
      setIsModalOpen(false);
    }
  };

  const displayedRepositories = searchQuery ? searchResults : repositories;

  return (
    <div className="min-h-screen bg-gray-950">
      <header className="bg-gray-900 border-b border-maroon-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Github className="h-8 w-8 text-maroon-500" />
              <h1 className="ml-3 text-2xl font-bold text-gray-100">
                GitHub Repository Manager
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <SearchBar searchQuery={searchQuery} onSearchChange={setSearchQuery} />
              <button
                onClick={() => setIsModalOpen(true)}
                className="inline-flex items-center px-4 py-2 border border-maroon-500 rounded-md shadow-sm text-sm font-medium text-maroon-200 bg-maroon-900 hover:bg-maroon-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-maroon-500 transition-colors"
              >
                <Plus className="h-5 w-5 mr-2" />
                Add Repository
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-12">
          <TrendingRepositories />
          {displayedRepositories.length > 0 && (
            <section>
              <h2 className="text-xl font-semibold text-gray-100 mb-4">
                {searchQuery ? 'Search Results' : 'Your Repositories'}
                <span className="ml-2 text-sm font-normal text-gray-400">
                  ({displayedRepositories.length}{' '}
                  {displayedRepositories.length === 1 ? 'repository' : 'repositories'})
                </span>
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {displayedRepositories.map((repo, index) => (
                  <div
                    key={index}
                    className="bg-gray-900 rounded-lg p-6 shadow-xl hover:shadow-2xl transition-all border border-maroon-800"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <h3 className="text-lg font-semibold text-gray-100">{repo.document_id.split("/").at(-1)}</h3>
                    </div>
                    <p className="text-gray-400">{repo.description}</p>

                    <div className="mt-4 flex items-center justify-between text-sm text-gray-400">
                      <div className="flex items-center">
                        <span className="mr-2 text-gray-500">Stars:</span>
                        <span className="text-yellow-500">{repo.stars}</span>
                      </div>
                      <div className="flex items-center">
                        <span className="mr-2 text-gray-500">Forks:</span>
                        <span>{repo.forks}</span>
                      </div>
                    </div>

                    <a
                      href={repo.document_id}
                      target='_blank'
                    >
                      <button 
                      className="mt-4 w-full bg-maroon-600 text-white py-2 rounded-md hover:bg-maroon-700 transition-all"
                      
                      >

                      Go to Repository
                      </button>
                    </a>
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>
      </main>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Add New Repository"
      >
        <RepositoryForm onSubmit={handleAddRepository} />
      </Modal>
    </div>
  );
}

export default App;
