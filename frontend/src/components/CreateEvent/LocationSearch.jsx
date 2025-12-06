import React, { useState } from 'react';
import SearchBar from './LocationSearch/SearchBar';
import MapView from './LocationSearch/MapView';

/**
 * Location Search Component - Combines search bar and map view
 */
export default function LocationSearch({
    searchQuery,
    onSearchQueryChange,
    onLocationSelect,
    formData,
    language
}) {
    return (
        <div className="location-search-container">
            <label>{language === 'en' ? 'Location Search' : 'חיפוש מיקום'}</label>

            <SearchBar
                searchQuery={searchQuery}
                onSearchQueryChange={onSearchQueryChange}
                onLocationSelect={onLocationSelect}
                language={language}
            />

            <MapView
                latitude={formData.latitude}
                longitude={formData.longitude}
                onLocationSelect={onLocationSelect}
                onSearchQueryChange={onSearchQueryChange}
                language={language}
            />
        </div>
    );
}
