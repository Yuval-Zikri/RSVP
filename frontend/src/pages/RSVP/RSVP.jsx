import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './RSVP.css';

export default function RSVP() {
    const { token } = useParams();
    const [invite, setInvite] = useState(null);
    const [event, setEvent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({
        status: 'attending',
        guests_count: 0
    });

    useEffect(() => {
        const fetchInvite = async () => {
            try {
                const res = await axios.get(`http://localhost:5000/api/rsvp/${token}`);
                setInvite(res.data.invitation);
                setEvent(res.data.event);
                setFormData({
                    status: res.data.invitation.status === 'pending' ? 'attending' : res.data.invitation.status,
                    guests_count: res.data.invitation.guests_count
                });
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchInvite();
    }, [token]);

    const handleSubmit = async () => {
        try {
            await axios.post(`http://localhost:5000/api/rsvp/${token}`, formData);
            alert('Thank you for your response!');
            window.location.reload();
        } catch (err) {
            alert('Error updating RSVP');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (!invite) return <div>Invalid Invitation Link</div>;

    return (
        <div className="rsvp-container card">
            <h1>{event.title}</h1>
            <p className="event-details">
                {new Date(event.date).toLocaleString()} @ {event.location}
            </p>

            <div className="guest-info">
                <p>Hello, <strong>{invite.name}</strong>!</p>
                <p>Current Status: <span className={`status-badge ${invite.status}`}>{invite.status}</span></p>
            </div>

            <div className="rsvp-form">
                <label>Will you attend?</label>
                <select
                    value={formData.status}
                    onChange={e => setFormData({ ...formData, status: e.target.value })}
                >
                    <option value="attending">Yes, I'll be there!</option>
                    <option value="not_attending">Sorry, can't make it</option>
                </select>

                {formData.status === 'attending' && (
                    <>
                        <label>How many additional guests?</label>
                        <input
                            type="number"
                            min="0"
                            value={formData.guests_count}
                            onChange={e => setFormData({ ...formData, guests_count: parseInt(e.target.value) })}
                        />
                    </>
                )}

                <button className="btn btn-primary" onClick={handleSubmit} style={{ marginTop: '20px' }}>
                    {invite.status === 'pending' ? 'Send RSVP' : 'Update RSVP'}
                </button>
            </div>
        </div>
    );
}
