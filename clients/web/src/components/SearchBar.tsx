import React, { useState } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/solid';

interface SearchBarProps {
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  return (
    <div className="max-w-lg mx-auto">
      <form onSubmit={handleSubmit} className="relative">
        <input
          type="text"
          placeholder="Search for a politician or billionaire..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full py-3 px-5 pr-12 rounded-full border-2 border-indigo-300 focus:border-indigo-500 focus:outline-none shadow-sm bg-white bg-opacity-90"
        />
        <button
          type="submit"
          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-indigo-500 hover:text-indigo-700"
        >
          <MagnifyingGlassIcon className="h-6 w-6" aria-hidden="true" />
          <span className="sr-only">Search</span>
        </button>
      </form>
    </div>
  );
};

export default SearchBar; 