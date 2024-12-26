import React from 'react';
import { ExternalLink, Tag, Star, GitFork } from 'lucide-react';

export function RepositoryCard({ repository }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start">
        <h1 className="text-lg font-semibold text-gray-900">{repository.title}</h1>
        <a
          href={repository.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 hover:text-blue-800"
        >
          <ExternalLink className="h-5 w-5" />
        </a>
      </div>

      <p className="mt-2 text-gray-600">{repository.description}</p>

      <div className="mt-4 flex flex-wrap gap-2">
        {repository.tags.map((tag, index) => (
          <span
            key={index}
            className="inline-flex items-center px-2.5 py-0.5 rounded-full 
                     text-xs font-medium bg-blue-100 text-blue-800"
          >
            <Tag className="h-3 w-3 mr-1" />
            {tag}
          </span>
        ))}
      </div>

      <div className="mt-4 flex items-center space-x-4 text-gray-500">
        <div className="flex items-center">
          <Star className="h-4 w-4 mr-1 text-yellow-500" />
          <span>{repository.stars}</span>
        </div>
        <div className="flex items-center">
          <GitFork className="h-4 w-4 mr-1 text-gray-500" />
          <span>{repository.forks}</span>
        </div>
      </div>

      <button
        onClick={() => window.open(repository.url, '_blank')}
        className="mt-4 w-full bg-maroon-600 text-white py-2 rounded-md hover:bg-maroon-700 transition-all"
      >
        Go to Repo
      </button>
    </div>
  );
}
