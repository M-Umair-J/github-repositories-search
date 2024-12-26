import React from 'react';
import { Flame, Star, GitFork } from 'lucide-react';

const TRENDING_REPOS = [
  {
    id: 'trending-1',
    title: 'Next.js 14 Enterprise Boilerplate',
    description: 'Production-ready template with advanced features, authentication, and best practices for large-scale applications.',
    url: 'https://github.com/vercel/next.js',
    tags: ['next.js', 'react', 'typescript', 'enterprise'],
    createdAt: new Date(),
    stars: '12.5k',
    forks: '892'
  },
  {
    id: 'trending-2',
    title: 'tRPC',
    description: 'End-to-end typesafe APIs made easy. A revolutionary way to build full-stack applications.',
    url: 'https://github.com/trpc/trpc',
    tags: ['typescript', 'api', 'fullstack'],
    createdAt: new Date(),
    stars: '8.2k',
    forks: '456'
  },
  {
    id: 'trending-3',
    title: 'Rust Web Template',
    description: 'Production-ready Rust web server template with built-in authentication, logging, and monitoring.',
    url: 'https://github.com/rust-lang/rust',
    tags: ['rust', 'web', 'template'],
    createdAt: new Date(),
    stars: '5.7k',
    forks: '234'
  }
];

export function TrendingRepositories() {
  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2">
        <Flame className="h-5 w-5 text-maroon-600" />
        <h2 className="text-xl font-semibold text-gray-100">Trending Repositories</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {TRENDING_REPOS.map((repo) => (
          <div key={repo.id} className="bg-gray-900 rounded-lg p-6 shadow-xl hover:shadow-2xl transition-all border border-maroon-800">
            <div className="flex justify-between items-start">
              <h3 className="text-lg font-semibold text-gray-100">{repo.title}</h3>
            </div>
            <p className="mt-2 text-gray-400">{repo.description}</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {repo.tags.map((tag, index) => (
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
                <span>{repo.stars}</span>
              </div>
              <div className="flex items-center">
                <GitFork className="h-4 w-4 mr-1" />
                <span>{repo.forks}</span>
              </div>
            </div>
            <button
              onClick={() => window.open(repo.url, '_blank')}
              className="mt-4 w-full bg-maroon-600 text-white py-2 rounded-md hover:bg-maroon-700 transition-all"
            >
              Visit Repo
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
