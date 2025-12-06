import React from 'react';

/**
 * Event Statistics Component - Displays RSVP statistics
 */
export default function EventStatistics({ rsvps, t }) {
    const attendingCount = rsvps.filter(r => r.status === 'attending').length;
    const totalPeople = rsvps
        .filter(r => r.status === 'attending')
        .reduce((sum, r) => sum + 1 + (r.guests_count || 0), 0);
    const pendingCount = rsvps.filter(r => r.status === 'pending').length;
    const declinedCount = rsvps.filter(r => r.status === 'not_attending').length;

    return (
        <div className="stats-grid">
            <div className="stat-box">
                <span className="stat-value">{attendingCount}</span>
                <span className="stat-label">{t.attending}</span>
            </div>
            <div className="stat-box">
                <span className="stat-value">{totalPeople}</span>
                <span className="stat-label">{t.totalPeople}</span>
            </div>
            <div className="stat-box">
                <span className="stat-value">{pendingCount}</span>
                <span className="stat-label">{t.pending}</span>
            </div>
            <div className="stat-box">
                <span className="stat-value">{declinedCount}</span>
                <span className="stat-label">{t.declined}</span>
            </div>
        </div>
    );
}
