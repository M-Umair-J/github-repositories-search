import { Flame } from 'lucide-react';
import { TrendingRepositoryCard } from './TrendingRepositoryCard';
import { TRENDING_REPOS } from './trending-data';

export function TrendingRepositories() {
  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2">
        <Flame className="h-5 w-5 text-maroon-600" />
        <h2 className="text-xl font-semibold text-gray-100">Trending Repositories</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {TRENDING_REPOS.map((repo) => (
          <TrendingRepositoryCard key={repo.id} repository={repo} />
        ))}
      </div>
    </div>
  );
}