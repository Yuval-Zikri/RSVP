import React, { useContext } from 'react';
import { getEventTypeName, getBackgrounds } from '../utils/eventTypes';
import { LanguageContext } from '../App';
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
            backgroundSize: 'contain',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat'
        };
    };

    return (
        <div className="preview-container card" style={{
            height: '100%',
            minHeight: '500px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            position: 'relative',
            overflow: 'hidden',
            backgroundColor: 'var(--bg-color)',
            ...getBackgroundImage()
        }}>
            <div className="preview-content" style={{
                padding: '2rem',
                background: 'rgba(255,255,255,0.95)',
                borderRadius: '16px',
                backdropFilter: 'blur(10px)',
                maxWidth: '80%',
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
                <h1 style={{ margin: '1rem 0', fontSize: '2.5rem', color: '#333' }}>
                    {title || 'Event Title'}
                </h1>
                <div className="preview-details" style={{ marginTop: '2rem' }}>
                    <p style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>
                        📅 {date ? new Date(date).toLocaleString() : 'Date & Time'}
                    </p>
                    <p style={{ fontSize: '1.2rem' }}>
                        📍 {location || 'Location'}
                    </p>
                </div>
                <div style={{ marginTop: '3rem' }}>
                    <button className="btn btn-primary" style={{ pointerEvents: 'none' }}>RSVP Now</button>
                </div>
            </div>
        </div>
    );
};

export default EventPreview;
