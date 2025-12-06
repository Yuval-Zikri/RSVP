import React from 'react';

/**
 * Reusable Button component with various styles
 */
export default function Button({
    children,
    variant = 'primary',
    size = 'medium',
    disabled = false,
    onClick,
    type = 'button',
    className = '',
    ...props
}) {
    const baseClass = 'btn';
    const variantClass = variant ? `btn-${variant}` : '';
    const sizeClass = size === 'small' ? 'btn-small' : '';

    const classes = [baseClass, variantClass, sizeClass, className]
        .filter(Boolean)
        .join(' ');

    return (
        <button
            type={type}
            className={classes}
            disabled={disabled}
            onClick={onClick}
            {...props}
        >
            {children}
        </button>
    );
}
