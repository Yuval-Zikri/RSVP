import React from 'react';
import { getAllEventTypes, getEventTypeName } from '../../utils/eventTypes';

/**
 * Event Type Selection Component (Step 0 of Create Event)
 */
export default function EventTypeSelector({ selectedType, onSelectType, language }) {
    return (
        <div className="event-type-selection">
            <p style={{ textAlign: 'center', marginBottom: '2rem', fontSize: '1.1rem', color: 'var(--text-color)' }}>
                {language === 'en' ? 'Select your event type' : 'בחר את סוג האירוע'}
            </p>
            <div className="event-type-grid">
                {getAllEventTypes().map(eventType => (
                    <div
                        key={eventType}
                        className={`event-type-card ${selectedType === eventType ? 'selected' : ''}`}
                        onClick={() => onSelectType(eventType)}
                    >
                        <div className="event-type-name-primary">{getEventTypeName(eventType, language)}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}
