import React, { useContext } from 'react';
import { getEventTypeName, getBackgrounds } from '../utils/eventTypes';
import { LanguageContext } from '../contexts';
import '../styles/theme.css';

const EventPreview = ({ formData }) => {
    const { language } = useContext(LanguageContext);
    const { title, date, location, type, background } = formData;

    const getBackgroundImage = () => {
        // Use selected background, or first available for the type
        let imageName = background;
        if (!imageName) {
            const backgrounds = getBackgrounds(type);
            imageName = backgrounds.length > 0 ? backgrounds[0] : null;
        }

        if (!imageName) return {};

        return {
            backgroundImage: `url(${new URL(`../background/${imageName}`, import.meta.url).href})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat'
        };
    };

    return (
        <div className="preview-container card" style={{
            width: '360px', // Fixed mobile width
            height: '640px', // Fixed mobile height (16:9 ratio)
            margin: '0 auto',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            position: 'relative',
            overflow: 'hidden',
            backgroundColor: 'var(--bg-color)',
            boxShadow: '0 20px 40px rgba(0,0,0,0.2)', // Enhanced shadow for "device" feel
            borderRadius: '20px', // Rounded corners like a phone
            ...getBackgroundImage()
        }}>
            <div className="preview-content" style={{
                padding: '1.5rem',
                background: 'rgba(255,255,255,0.95)',
                borderRadius: '16px',
                backdropFilter: 'blur(10px)',
                maxWidth: '400px', // Reduced width to show more background
                width: '90%',
                zIndex: 2,
                position: 'relative',
                boxShadow: '0 8px 32px rgba(0,0,0,0.1)'
            }}>
                <span className="badge" style={{
                    textTransform: 'uppercase',
                    fontSize: '0.8rem',
                    letterSpacing: '2px',
                    color: '#666',
                    fontWeight: 'bold'
                }}>
                    {getEventTypeName(type, language)}
                </span>
                <h1 style={{ margin: '1rem 0', fontSize: '2.5rem', color: '#333', lineHeight: 1.2 }}>
                    {title || 'Event Title'}
                </h1>
                {formData.subtitle && (
                    <h2 style={{
                        margin: '0 0 2rem 0',
                        fontSize: '1.5rem',
                        color: '#666',
                        fontFamily: 'Georgia, serif',
                        fontStyle: 'italic',
                        fontWeight: 'normal'
                    }}>
                        {formData.subtitle}
                    </h2>
                )}
                <div className="preview-details" style={{ marginTop: '2rem', textAlign: 'left', display: 'inline-block', color: '#333' }}>
                    <p style={{ fontSize: '1.1rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center' }}>
                        <span style={{ marginRight: '10px', fontSize: '1.2rem' }}>📅</span>
                        {date ? new Date(date).toLocaleString() : 'Date & Time'}
                    </p>
                    <p style={{ fontSize: '1.1rem', display: 'flex', alignItems: 'center' }}>
                        <span style={{ marginRight: '10px', fontSize: '1.2rem' }}>📍</span>
                        {location || 'Location'}
                    </p>
                </div>

                <div style={{ marginTop: '2.5rem' }}>
                    <button className="btn btn-primary" style={{ pointerEvents: 'none', width: '100%', padding: '12px', borderRadius: '50px', fontWeight: 'bold' }}>RSVP Now</button>
                </div>

                <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'center', gap: '10px' }}>
                    <button className="btn btn-outline" style={{
                        fontSize: '0.9rem',
                        padding: '8px 16px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px',
                        background: 'white',
                        border: '1px solid #007bff',
                        color: '#007bff',
                        borderRadius: '50px',
                        cursor: 'pointer'
                    }}>
                        🚗 Waze
                    </button>
                    <button className="btn btn-outline" style={{
                        fontSize: '0.9rem',
                        padding: '8px 16px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px',
                        background: 'white',
                        border: '1px solid #007bff',
                        color: '#007bff',
                        borderRadius: '50px',
                        cursor: 'pointer'
                    }}>
                        🗺️ Maps
                    </button>
                </div>
            </div>
        </div>
    );
};

export default EventPreview;
