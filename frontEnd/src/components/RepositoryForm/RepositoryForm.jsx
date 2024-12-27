import { useState } from 'react';
import PropTypes from 'prop-types';

export function RepositoryForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    url: '',
    tags: '',
    stars: '',
    forks: '',
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      ...formData,
      stars: parseInt(formData.stars, 10),
      forks: parseInt(formData.forks, 10),
      tags: formData.tags.split(',').map((tag) => tag.trim()),
    });
    setFormData({ title: '', description: '', url: '', tags: '', stars: '', forks: '' });
  };

  const isValidUrl = (url) => {
    try {
      new URL(url);
      return url.includes('github.com');
    } catch {
      return false;
    }
  };

  const isFormValid = () => {
    return (
      formData.title.trim() !== '' &&
      formData.description.trim() !== '' &&
      isValidUrl(formData.url) &&
      formData.stars !== '' &&
      !isNaN(formData.stars) &&
      formData.forks !== '' &&
      !isNaN(formData.forks)
    );
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-300">
          Repository Title *
        </label>
        <input
          type="text"
          id="title"
          required
          className="mt-1 block w-full rounded-md border-maroon-700 bg-gray-800 
                   text-gray-100 shadow-sm focus:border-maroon-500 focus:ring-maroon-500"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-300">
          Description *
        </label>
        <textarea
          id="description"
          required
          rows={3}
          className="mt-1 block w-full rounded-md border-maroon-700 bg-gray-800 
                   text-gray-100 shadow-sm focus:border-maroon-500 focus:ring-maroon-500"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
        />
      </div>

      <div>
        <label htmlFor="url" className="block text-sm font-medium text-gray-300">
          GitHub URL *
        </label>
        <input
          type="url"
          id="url"
          required
          pattern="https://github\.com/.*"
          className="mt-1 block w-full rounded-md border-maroon-700 bg-gray-800 
                   text-gray-100 shadow-sm focus:border-maroon-500 focus:ring-maroon-500"
          value={formData.url}
          onChange={(e) => setFormData({ ...formData, url: e.target.value })}
        />
      </div>

      <div>
        <label htmlFor="tags" className="block text-sm font-medium text-gray-300">
          Tags (comma-separated)
        </label>
        <input
          type="text"
          id="tags"
          className="mt-1 block w-full rounded-md border-maroon-700 bg-gray-800 
                   text-gray-100 shadow-sm focus:border-maroon-500 focus:ring-maroon-500"
          value={formData.tags}
          onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
          placeholder="react, typescript, frontend..."
        />
      </div>

      <div>
        <label htmlFor="stars" className="block text-sm font-medium text-gray-300">
          Stars *
        </label>
        <input
          type="number"
          id="stars"
          required
          min="0"
          className="mt-1 block w-full rounded-md border-maroon-700 bg-gray-800 
                   text-gray-100 shadow-sm focus:border-maroon-500 focus:ring-maroon-500"
          value={formData.stars}
          onChange={(e) => setFormData({ ...formData, stars: e.target.value })}
        />
      </div>

      <div>
        <label htmlFor="forks" className="block text-sm font-medium text-gray-300">
          Forks *
        </label>
        <input
          type="number"
          id="forks"
          required
          min="0"
          className="mt-1 block w-full rounded-md border-maroon-700 bg-gray-800 
                   text-gray-100 shadow-sm focus:border-maroon-500 focus:ring-maroon-500"
          value={formData.forks}
          onChange={(e) => setFormData({ ...formData, forks: e.target.value })}
        />
      </div>

      <button
        type="submit"
        disabled={!isFormValid()}
        className="w-full inline-flex justify-center items-center px-4 py-2 border 
                 border-transparent text-sm font-medium rounded-md shadow-sm text-white 
                 bg-maroon-600 hover:bg-maroon-700 focus:outline-none focus:ring-2 
                 focus:ring-offset-2 focus:ring-maroon-500 disabled:opacity-50
                 disabled:cursor-not-allowed transition-colors"
      >
        Add Repository
      </button>
    </form>
  );
}

RepositoryForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
};