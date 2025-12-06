import React from 'react';

/**
 * Events List Component - Shows list of events in sidebar
 */
export default function EventsList({
    events,
    selectedEvent,
    onSelectEvent,
    onEditEvent,
    onDeleteEvent,
    t
}) {
    return (
        <div className="events-list card">
            <h3>{t.yourEvents}</h3>
            {events.length === 0 && <p>{t.noEvents}</p>}
            {events.map(ev => (
                <div
                    key={ev.id}
                    className={`event-item ${selectedEvent?.id === ev.id ? 'active' : ''}`}
                    onClick={() => onSelectEvent(ev)}
                >
                    <div className="event-item-content">
                        <h4>{ev.title}</h4>
                        <p>{new Date(ev.date).toLocaleDateString()}</p>
                    </div>
                    <div className="event-item-actions">
                        <button
                            className="btn-edit"
                            onClick={(e) => onEditEvent(e, ev)}
                            title={t.editEvent}
                        >
                            ✏️
                        </button>
                        <button
                            className="btn-delete"
                            onClick={(e) => onDeleteEvent(e, ev.id)}
                            title={t.deleteEvent}
                        >
                            🗑️
                        </button>
                    </div>
                </div>
            ))}
        </div>
    );
}
