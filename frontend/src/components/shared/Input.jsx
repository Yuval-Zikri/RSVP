import React from 'react';

/**
 * Reusable Input component
 */
export default function Input({
    label,
    type = 'text',
    value,
    onChange,
    placeholder,
    required = false,
    disabled = false,
    className = '',
    ...props
}) {
    return (
        <div className={`form-group ${className}`}>
            {label && <label>{label}</label>}
            <input
                type={type}
                value={value}
                onChange={onChange}
                placeholder={placeholder}
                required={required}
                disabled={disabled}
                {...props}
            />
        </div>
    );
}
