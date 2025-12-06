import React from 'react';
import { OpenStreetMapProvider } from 'leaflet-geosearch';
import axios from 'axios';

/**
 * Search Bar Component - Input, button, and results list
 */
export default function SearchBar({
    searchQuery,
    onSearchQueryChange,
    onLocationSelect,
    language
}) {
    const [searchResults, setSearchResults] = React.useState([]);
    const [loading, setLoading] = React.useState(false);

    const handleSearch = async () => {
        if (!searchQuery) return;
        setLoading(true);

        try {
            // OpenStreetMap Search
            const provider = new OpenStreetMapProvider({
                params: {
                    'accept-language': 'he',
                    countrycodes: 'il',
                    addressdetails: 1,
                },
            });

            const osmPromise = provider.search({ query: searchQuery })
                .catch(err => {
                    console.error("OSM search failed", err);
                    return [];
                });

            // Waze Search (via Backend)
            const wazePromise = axios.get(`/api/search-location?q=${encodeURIComponent(searchQuery)}`)
                .then(res => res.data || [])
                .catch(err => {
                    console.error("Waze search failed", err);
                    return [];
                });

            // Run both in parallel
            const [osmResults, wazeResults] = await Promise.all([osmPromise, wazePromise]);

            // Combine results (Waze first as it might be more relevant for local places)
            const allResults = [...wazeResults, ...osmResults];
            const uniqueResults = Array.from(new Map(allResults.map(item => [item.label, item])).values());

            setSearchResults(uniqueResults);
        } catch (error) {
            console.error("Search failed", error);
        } finally {
            setLoading(false);
        }
    };

    const selectLocation = (result) => {
        onLocationSelect({
            location: result.label.split(',')[0],
            address: result.label,
            latitude: parseFloat(result.y),
            longitude: parseFloat(result.x)
        });
        setSearchResults([]);
        onSearchQueryChange(result.label);
    };

    return (
        <>
            <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
                <input
                    value={searchQuery}
                    onChange={e => onSearchQueryChange(e.target.value)}
                    placeholder={language === 'en' ? 'Search for a place...' : 'חפש כתובת או מקום...'}
                    style={{ flex: 1 }}
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                />
                <button className="btn btn-secondary" onClick={handleSearch}>
                    🔍
                </button>
            </div>

            {searchResults.length > 0 && (
                <ul className="search-results-list">
                    {searchResults.map((result, idx) => (
                        <li key={idx} onClick={() => selectLocation(result)}>
                            {result.label}
                        </li>
                    ))}
                </ul>
            )}
        </>
    );
}
