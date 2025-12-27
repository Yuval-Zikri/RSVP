import React, { useState } from 'react';
import { getAllEventTypes, getEventTypeName } from '../../utils/eventTypes';
import BackgroundSelector from './BackgroundSelector';
import LocationSearch from './LocationSearch';

/**
 * Event Details Form Component (Step 1 of Create Event)
 */
export default function EventDetailsForm({ formData, onFormDataChange, language }) {
    const [searchQuery, setSearchQuery] = useState('');

    const handleLocationSelect = React.useCallback((locationData) => {
        onFormDataChange(prev => ({
            ...prev,
            ...locationData
        }));
    }, [onFormDataChange]);

    return (
        <div className="form-step">
            <label>{language === 'en' ? 'Event Title' : 'שם האירוע'}</label>
            <input
                name="title"
                value={formData.title}
                onChange={e => onFormDataChange({ ...formData, title: e.target.value })}
                placeholder={language === 'en' ? "e.g. Yuval's Wedding" : "לדוגמה: החתונה של יובל"}
            />

            <label>{language === 'en' ? 'Subtitle / Hosts' : 'תת כותרת / מארחים'}</label>
            <input
                name="subtitle"
                value={formData.subtitle}
                onChange={e => onFormDataChange({ ...formData, subtitle: e.target.value })}
                placeholder={language === 'en' ? "e.g. Hila & Ido" : "לדוגמה: הילה & עידו"}
            />

            <label>{language === 'en' ? 'Type' : 'סוג'}</label>
            <select value={formData.type} onChange={e => onFormDataChange({ ...formData, type: e.target.value, background: '' })}>
                {getAllEventTypes().map(eventType => (
                    <option key={eventType} value={eventType}>
                        {getEventTypeName(eventType, language)}
                    </option>
                ))}
            </select>

            <BackgroundSelector
                eventType={formData.type}
                selectedBackground={formData.background}
                onSelectBackground={(bg) => onFormDataChange({ ...formData, background: bg })}
                language={language}
            />

            <label style={{ marginTop: '20px' }}>{language === 'en' ? 'Date' : 'תאריך'}</label>
            <input
                name="date"
                type="datetime-local"
                value={formData.date}
                onChange={e => onFormDataChange({ ...formData, date: e.target.value })}
                min={new Date().toISOString().slice(0, 16)}
            />

            <LocationSearch
                searchQuery={searchQuery}
                onSearchQueryChange={setSearchQuery}
                onLocationSelect={handleLocationSelect}
                formData={formData}
                language={language}
            />
        </div>
    );
}
