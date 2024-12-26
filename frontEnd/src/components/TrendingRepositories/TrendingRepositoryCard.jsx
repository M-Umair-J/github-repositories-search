import PropTypes from 'prop-types';
import { Star, GitFork } from 'lucide-react';

export function TrendingRepositoryCard({ repository }) {
  return (
    <div className="bg-gray-900 rounded-lg p-6 shadow-xl hover:shadow-2xl transition-all border border-maroon-800">
      <div className="flex justify-between items-start">
        <h3 className="text-lg font-semibold text-gray-100">{repository.title}</h3>
      </div>
      <p className="mt-2 text-gray-400">{repository.description}</p>
      <div className="mt-4 flex flex-wrap gap-2">
        {repository.tags.map((tag, index) => (
          <span
            key={index}
            className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-maroon-900 text-maroon-200"
          >
            {tag}
          </span>
        ))}
      </div>
      <div className="mt-4 flex items-center space-x-4 text-gray-400">
        <div className="flex items-center">
          <Star className="h-4 w-4 mr-1" />
          <span>{repository.stars}</span>
        </div>
        <div className="flex items-center">
          <GitFork className="h-4 w-4 mr-1" />
          <span>{repository.forks}</span>
        </div>
      </div>
    </div>
  );
}

TrendingRepositoryCard.propTypes = {
  repository: PropTypes.shape({
    id: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    tags: PropTypes.arrayOf(PropTypes.string).isRequired,
    stars: PropTypes.string.isRequired,
    forks: PropTypes.string.isRequired,
  }).isRequired,
};