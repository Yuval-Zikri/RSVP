import React from 'react';
import { getBackgrounds } from '../../utils/eventTypes';

/**
 * Background Selector Component
 */
export default function BackgroundSelector({ eventType, selectedBackground, onSelectBackground, language }) {
    const backgrounds = getBackgrounds(eventType);

    return (
        <div>
            <label>{language === 'en' ? 'Choose Background' : 'בחר רקע'}</label>
            <div className="background-grid" style={{ marginTop: '10px' }}>
                {backgrounds.map((bg, index) => (
                    <div
                        key={bg}
                        className={`bg-option ${selectedBackground === bg ? 'selected' : ''}`}
                        onClick={() => onSelectBackground(bg)}
                        style={{
                            backgroundImage: `url(${new URL(`../../background/${bg}`, import.meta.url).href})`,
                            backgroundSize: 'cover',
                            backgroundPosition: 'center',
                            minHeight: '100px'
                        }}
                    >
                        {!selectedBackground && index === 0 && (
                            <span style={{
                                background: 'rgba(255,255,255,0.8)',
                                padding: '5px',
                                borderRadius: '4px',
                                fontSize: '0.8rem'
                            }}>
                                Default
                            </span>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}
