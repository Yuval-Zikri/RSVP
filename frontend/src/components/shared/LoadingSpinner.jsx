import React from 'react';

/**
 * Loading spinner component
 */
export default function LoadingSpinner({ size = 'medium', text = '' }) {
    const sizeClass = size === 'small' ? '20px' : size === 'large' ? '60px' : '40px';

    const spinnerStyle = {
        border: '3px solid var(--border-color)',
        borderTop: '3px solid var(--primary-color)',
        borderRadius: '50%',
        width: sizeClass,
        height: sizeClass,
        animation: 'spin 1s linear infinite',
        margin: 'auto'
    };

    return (
        <div style={{ textAlign: 'center', padding: '20px' }}>
            <div style={spinnerStyle}></div>
            {text && <p style={{ marginTop: '10px', color: 'var(--text-color)' }}>{text}</p>}
            <style>{`
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `}</style>
        </div>
    );
}
