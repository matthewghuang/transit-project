import React, { useState, useEffect, useRef } from 'react';
import ky from 'ky';

interface StopResult {
  id: string;
  name: string;
  observation_count: number;
  routes: string[];
}

interface HeroSearchProps {
  onSelectStop: (stopId: string) => void;
}

export const HeroSearch: React.FC<HeroSearchProps> = ({ onSelectStop }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<StopResult[]>([]);
  const [recentSearches, setRecentSearches] = useState<StopResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const saved = localStorage.getItem('recent_searches');
    if (saved) {
      try {
        setRecentSearches(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse recent searches', e);
      }
    }
  }, []);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setResults([]);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (query.length < 2) {
      setResults([]);
      return;
    }

    const timer = setTimeout(async () => {
      setIsLoading(true);
      try {
        const data = await ky.get(`/api/stops/search?q=${encodeURIComponent(query)}`).json<StopResult[]>();
        setResults(data);
      } catch (e) {
        console.error('Search failed', e);
      } finally {
        setIsLoading(false);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  const handleSelect = (stop: StopResult) => {
    // Save to recent searches
    const updated = [stop, ...recentSearches.filter(s => s.id !== stop.id)].slice(0, 5);
    setRecentSearches(updated);
    localStorage.setItem('recent_searches', JSON.stringify(updated));
    
    setQuery('');
    setResults([]);
    onSelectStop(stop.id);
  };

  const handleRemoveRecent = (e: React.MouseEvent, stopId: string) => {
    e.stopPropagation();
    const updated = recentSearches.filter(s => s.id !== stopId);
    setRecentSearches(updated);
    localStorage.setItem('recent_searches', JSON.stringify(updated));
  };

  return (
    <div className="hero-container">
      <div className="hero-content">
        <h1>Where is your bus?</h1>
        <p>Real-time reliability data for Translink stops</p>
        
        <div className="search-wrapper" ref={dropdownRef}>
          <input
            type="text"
            className="hero-search-input"
            placeholder="Search by stop name or 5-digit ID..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          
          {(results.length > 0 || isLoading) && (
            <div className="search-results">
              {isLoading && <div className="search-loading">Searching...</div>}
              {results.map(stop => (
                <div key={stop.id} className="search-result-item" onClick={() => handleSelect(stop)}>
                  <div className="stop-name">{stop.name}</div>
                  <div className="stop-meta">
                    <span className="stop-id">#{stop.id}</span>
                    <span className="stop-routes">{stop.routes.join(', ')}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {recentSearches.length > 0 && query.length === 0 && (
          <div className="recent-searches">
            <h3>Recent Searches</h3>
            <div className="recent-tags">
              {recentSearches.map(stop => (
                <div key={stop.id} className="tag-wrapper">
                  <button className="tag-btn" onClick={() => onSelectStop(stop.id)}>
                    {stop.name}
                  </button>
                  <button 
                    className="tag-remove-btn" 
                    onClick={(e) => handleRemoveRecent(e, stop.id)}
                    aria-label={`Remove ${stop.name} from recent searches`}
                  >
                    &times;
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
