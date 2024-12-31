import React from 'react';
import { Search } from 'lucide-react';

export function SearchBar({ searchQuery, onSearchChange,fetchSearchResults }) {
  console.log(fetchSearchResults);
  return (
    <div className="relative w-full max-w-xl">
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <Search className="h-5 w-5 text-gray-400" />
      </div>
      <input
        type="text"
        className="block w-full pl-10 pr-3 py-2 border border-maroon-700 rounded-lg 
                 bg-gray-900 text-gray-100 shadow-sm focus:outline-none focus:ring-2 
                 focus:ring-maroon-500 focus:border-transparent placeholder-gray-500"
        placeholder="Search repositories..."
        value={searchQuery}
        onChange={(e) => onSearchChange(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            fetchSearchResults();
          }
        }} 
      />
    </div>
  );
}
