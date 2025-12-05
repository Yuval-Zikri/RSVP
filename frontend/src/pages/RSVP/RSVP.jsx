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
                const res = await axios.get(`/api/rsvp/${token}`);
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

        // Set default theme to dark
        if (!document.body.getAttribute('data-theme')) {
            document.body.setAttribute('data-theme', 'dark');
        }
    }, [token]);

    const handleSubmit = async () => {
        try {
            await axios.post(`/api/rsvp/${token}`, formData);
            alert('Thank you for your response!');
            window.location.reload();
        } catch (err) {
            alert('Error updating RSVP');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (!invite) return <div>Invalid Invitation Link</div>;

    const toggleTheme = () => {
        const newTheme = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', newTheme);
    };

    // Convert filename to local URL
    const getBackgroundUrl = (filename) => {
        try {
            return new URL(`../../background/${filename}`, import.meta.url).href;
        } catch {
            return filename; // Fallback if it's already a URL
        }
    };

    return (
        <div className="rsvp-page-wrapper">
            <div className="rsvp-phone-container" style={{ backgroundImage: `url(${getBackgroundUrl(event.background_theme)})` }}>
                <button className="theme-toggle-btn" onClick={toggleTheme}>
                    🌓
                </button>

                <div className="rsvp-card">
                    <div className="event-header">
                        <span className="event-label">WEDDING</span>
                        <h1>{event.title}</h1>
                    </div>

                    <div className="event-info">
                        <div className="info-item">
                            <span className="icon">📅</span>
                            <p>{new Date(event.date).toLocaleString()}</p>
                        </div>
                        <div className="info-item">
                            <span className="icon">📍</span>
                            <p>{event.location}</p>
                        </div>
                    </div>

                    <div className="location-actions">
                        {event.latitude && event.longitude ? (
                            <>
                                <a
                                    href={`https://waze.com/ul?ll=${event.latitude},${event.longitude}&navigate=yes`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="btn-location waze"
                                >
                                    Navigate with Waze
                                </a>
                                <a
                                    href={`https://www.google.com/maps/search/?api=1&query=${event.latitude},${event.longitude}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="btn-location google"
                                >
                                    Google Maps
                                </a>
                            </>
                        ) : (
                            <>
                                <a
                                    href={`https://waze.com/ul?q=${encodeURIComponent(event.location)}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="btn-location waze"
                                >
                                    Navigate with Waze
                                </a>
                                <a
                                    href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(event.location)}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="btn-location google"
                                >
                                    Google Maps
                                </a>
                            </>
                        )}
                    </div>

                    <div className="guest-welcome">
                        <p>Hello <strong>{invite.name}</strong>,</p>
                        <p>We would love to see you there!</p>
                    </div>

                    <div className="rsvp-form-section">
                        <select
                            value={formData.status}
                            onChange={e => setFormData({ ...formData, status: e.target.value })}
                            className="status-select"
                        >
                            <option value="attending">✅ I'll be there</option>
                            <option value="not_attending">❌ Can't make it</option>
                        </select>

                        {formData.status === 'attending' && (
                            <div className="guests-input">
                                <label>Additional Guests:</label>
                                <input
                                    type="number"
                                    min="0"
                                    value={formData.guests_count}
                                    onChange={e => setFormData({ ...formData, guests_count: parseInt(e.target.value) })}
                                />
                            </div>
                        )}

                        <button className="btn-submit" onClick={handleSubmit}>
                            {invite.status === 'pending' ? 'RSVP Now' : 'Update RSVP'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
