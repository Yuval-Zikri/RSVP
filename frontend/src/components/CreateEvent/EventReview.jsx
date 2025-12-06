import React from 'react';

/**
 * Event Review/Summary Component (Step 3 of Create Event)
 */
export default function EventReview({ formData, onSubmit, loading, language }) {
    return (
        <div className="review-step">
            <h3>{language === 'en' ? 'Summary' : 'סיכום'}</h3>
            <p><strong>{language === 'en' ? 'Event:' : 'אירוע:'}</strong> {formData.title}</p>
            <p><strong>{language === 'en' ? 'Date:' : 'תאריך:'}</strong> {formData.date}</p>
            <p><strong>{language === 'en' ? 'Guests:' : 'אורחים:'}</strong> {formData.guests.length}</p>
            <button className="btn btn-primary" onClick={onSubmit} disabled={loading}>
                {loading
                    ? (language === 'en' ? 'Sending...' : 'שולח...')
                    : (language === 'en' ? 'Confirm & Send Invitations' : 'אשר ושלח הזמנות')
                }
            </button>
        </div>
    );
}
