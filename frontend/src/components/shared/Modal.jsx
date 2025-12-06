import React from 'react';

/**
 * Reusable Modal component
 */
export default function Modal({
    isOpen,
    onClose,
    title,
    children,
    size = 'medium', // 'medium' or 'large'
    showCloseButton = true
}) {
    if (!isOpen) return null;

    const modalSizeClass = size === 'large' ? 'modal-large' : '';

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div
                className={`modal-content ${modalSizeClass}`}
                onClick={(e) => e.stopPropagation()}
            >
                {title && (
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        marginBottom: '1rem'
                    }}>
                        <h2>{title}</h2>
                        {showCloseButton && (
                            <button
                                className="btn btn-secondary"
                                onClick={onClose}
                            >
                                Close
                            </button>
                        )}
                    </div>
                )}
                {children}
            </div>
        </div>
    );
}
