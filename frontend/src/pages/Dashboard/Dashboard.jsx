import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dashboard.css';

export default function Dashboard() {
    const [events, setEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [rsvps, setRsvps] = useState([]); // Mock data for now, ideally fetched from backend

    useEffect(() => {
        fetchEvents();
    }, []);

    const fetchEvents = async () => {
        try {
            const res = await axios.get('http://localhost:5000/api/events');
            setEvents(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    // Mock function to simulate fetching RSVPs for an event
    // In real app, we'd have GET /api/events/:id/rsvps
    const handleSelectEvent = (event) => {
        setSelectedEvent(event);
        // TODO: Fetch real RSVPs
        setRsvps([
            { name: 'John Doe', email: 'john@example.com', status: 'attending', guests: 2 },
            { name: 'Jane Smith', email: 'jane@example.com', status: 'pending', guests: 0 },
            { name: 'Bob Wilson', email: 'bob@example.com', status: 'not_attending', guests: 0 },
        ]);
    };

    const sendReminder = (email) => {
        alert(`Reminder sent to ${email}`);
        // axios.post('/api/reminders', { email, event_id: selectedEvent.id })
    };

    return (
        <div className="dashboard-container">
            <div className="events-list card">
                <h3>Your Events</h3>
                {events.map(ev => (
                    <div
                        key={ev.id}
                        className={`event-item ${selectedEvent?.id === ev.id ? 'active' : ''}`}
                        onClick={() => handleSelectEvent(ev)}
                    >
                        <h4>{ev.title}</h4>
                        <p>{new Date(ev.date).toLocaleDateString()}</p>
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
                                <span className="stat-value">{rsvps.filter(r => r.status === 'pending').length}</span>
                                <span className="stat-label">Pending</span>
                            </div>
                        </div>

                        <h4>Guest List</h4>
                        <table className="rsvp-table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Status</th>
                                    <th>Guests</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {rsvps.map((r, i) => (
                                    <tr key={i}>
                                        <td>{r.name}</td>
                                        <td>
                                            <span className={`status-badge ${r.status}`}>{r.status}</span>
                                        </td>
                                        <td>{r.guests}</td>
                                        <td>
                                            {r.status === 'pending' && (
                                                <button className="btn-small" onClick={() => sendReminder(r.email)}>Remind</button>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </>
                ) : (
                    <p>Select an event to view details</p>
                )}
            </div>
        </div>
    );
}
