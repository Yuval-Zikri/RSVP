import React, { useState, useEffect } from 'react';
import axios from 'axios';
import * as XLSX from 'xlsx';
import './Dashboard.css';

export default function Dashboard() {
    const [events, setEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [rsvps, setRsvps] = useState([]);

    useEffect(() => {
        fetchEvents();
    }, []);

    const fetchEvents = async () => {
        try {
            const res = await axios.get('/api/events');
            setEvents(res.data);
            if (selectedEvent) {
                // Check if selected event still exists
                const stillExists = res.data.find(e => e.id === selectedEvent.id);
                if (!stillExists) setSelectedEvent(null);
            }
        } catch (err) {
            console.error(err);
        }
    };

    const handleSelectEvent = async (event) => {
        setSelectedEvent(event);
        try {
            const res = await axios.get(`/api/events/${event.id}/rsvps`);
            setRsvps(res.data);
        } catch (err) {
            console.error("Failed to fetch RSVPs", err);
            setRsvps([]);
        }
    };

    const handleDeleteEvent = async (e, eventId) => {
        e.stopPropagation(); // Prevent triggering handleSelectEvent
        if (window.confirm('Are you sure you want to delete this event?')) {
            try {
                await axios.delete(`/api/events/${eventId}`);
                fetchEvents(); // Refresh list
                if (selectedEvent?.id === eventId) {
                    setSelectedEvent(null);
                    setRsvps([]);
                }
            } catch (err) {
                console.error("Failed to delete event", err);
                alert('Failed to delete event');
            }
        }
    };

    const sendReminder = (email) => {
        alert(`Reminder sent to ${email}`);
        // axios.post('/api/reminders', { email, event_id: selectedEvent.id })
    };

    const handleRemindAll = () => {
        const pendingRsvps = rsvps.filter(r => r.status === 'pending');
        if (pendingRsvps.length === 0) {
            alert('No pending RSVPs to remind');
            return;
        }

        if (window.confirm(`Send reminders to ${pendingRsvps.length} pending guests?`)) {
            pendingRsvps.forEach(r => sendReminder(r.email));
            alert(`Sent reminders to ${pendingRsvps.length} guests`);
        }
    };

    const handleExportToExcel = () => {
        if (rsvps.length === 0) {
            alert('No data to export');
            return;
        }

        const exportData = rsvps.map(r => ({
            Name: r.name,
            Email: r.email,
            Status: r.status,
            Guests: r.guests_count || 0,
            Total: r.status === 'attending' ? (1 + (r.guests_count || 0)) : 0
        }));

        const ws = XLSX.utils.json_to_sheet(exportData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Guest List");
        XLSX.writeFile(wb, `${selectedEvent.title}_guests.xlsx`);
    };

    return (
        <div className="dashboard-container">
            <div className="events-list card">
                <h3>Your Events</h3>
                {events.length === 0 && <p>No events found.</p>}
                {events.map(ev => (
                    <div
                        key={ev.id}
                        className={`event-item ${selectedEvent?.id === ev.id ? 'active' : ''}`}
                        onClick={() => handleSelectEvent(ev)}
                    >
                        <div className="event-item-content">
                            <h4>{ev.title}</h4>
                            <p>{new Date(ev.date).toLocaleDateString()}</p>
                        </div>
                        <button
                            className="btn-delete"
                            onClick={(e) => handleDeleteEvent(e, ev.id)}
                            title="Delete Event"
                        >
                            🗑️
                        </button>
                    </div>
                ))}
            </div>

            <div className="event-details card">
                {selectedEvent ? (
                    <>
                        <h3>{selectedEvent.title} - Dashboard</h3>
                        <div className="stats-grid">
                            <div className="stat-box">
                                <span className="stat-value">{rsvps.filter(r => r.status === 'attending').length}</span>
                                <span className="stat-label">Attending</span>
                            </div>
                            <div className="stat-box">
                                <span className="stat-value">
                                    {rsvps
                                        .filter(r => r.status === 'attending')
                                        .reduce((sum, r) => sum + 1 + (r.guests_count || 0), 0)
                                    }
                                </span>
                                <span className="stat-label">Total People</span>
                            </div>
                            <div className="stat-box">
                                <span className="stat-value">{rsvps.filter(r => r.status === 'pending').length}</span>
                                <span className="stat-label">Pending</span>
                            </div>
                            <div className="stat-box">
                                <span className="stat-value">{rsvps.filter(r => r.status === 'not_attending').length}</span>
                                <span className="stat-label">Declined</span>
                            </div>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                            <h4 style={{ margin: 0 }}>Guest List</h4>
                            <div style={{ display: 'flex', gap: '10px' }}>
                                <button
                                    className="btn btn-secondary"
                                    onClick={handleRemindAll}
                                    disabled={rsvps.filter(r => r.status === 'pending').length === 0}
                                >
                                    📧 Remind All Pending
                                </button>
                                <button
                                    className="btn btn-primary"
                                    onClick={handleExportToExcel}
                                    disabled={rsvps.length === 0}
                                >
                                    📊 Export to Excel
                                </button>
                            </div>
                        </div>
                        <div className="table-responsive">
                            <table className="rsvp-table">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Status</th>
                                        <th>Guests</th>
                                        <th>Total</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {rsvps.map((r, i) => (
                                        <tr key={i}>
                                            <td>{r.name} <span style={{ fontSize: '0.8em', color: '#666' }}>({r.email})</span></td>
                                            <td>
                                                <span className={`status-badge ${r.status}`}>{r.status}</span>
                                            </td>
                                            <td>{r.guests_count}</td>
                                            <td>
                                                {r.status === 'attending' ? (1 + (r.guests_count || 0)) : '-'}
                                            </td>
                                            <td>
                                                {r.status === 'pending' && (
                                                    <button className="btn-small" onClick={() => sendReminder(r.email)}>Remind</button>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                    {rsvps.length === 0 && (
                                        <tr>
                                            <td colSpan="5" style={{ textAlign: 'center' }}>No guests found for this event.</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </>
                ) : (
                    <p>Select an event to view details</p>
                )}
            </div>
        </div>
    );
}
