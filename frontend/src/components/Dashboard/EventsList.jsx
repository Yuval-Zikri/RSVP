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
    onDeleteAllEvents,
    t
}) {
    return (
        <div className="events-list card">
            <h3>{t.yourEvents}</h3>
            <div className="events-scroll-area">
                {events.length === 0 && <p style={{ padding: '20px' }}>{t.noEvents}</p>}
                {events.map(ev => (
                    <div
                        key={ev.id}
                        data-event-id={ev.id}
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

            <div className="events-list-footer">
                <button
                    className="btn btn-danger w-100"
                    onClick={onDeleteAllEvents}
                    disabled={events.length === 0}
                >
                    🗑️ {t.deleteAllEvents}
                </button>
            </div>
        </div>
    );
}
