import React, { useState, useContext } from 'react';
import * as XLSX from 'xlsx';
import axios from 'axios';
import './CreateEvent.css';
import EventPreview from '../../components/EventPreview';
import { LanguageContext } from '../../App';

import EVENT_TYPES, { getAllEventTypes, getEventTypeName, getBackgrounds } from '../../utils/eventTypes';

export default function CreateEvent() {
    const context = useContext(LanguageContext);
    const language = context?.language || 'en'; // Default to 'en' if context is not available
    const [step, setStep] = useState(0);
    const [formData, setFormData] = useState({
        title: '',
        type: 'wedding',
        background: '', // Selected background image
        date: '',
        location: '',
        guests: [] // Array of {name, email}
    });
    const [loading, setLoading] = useState(false);

    const handleNext = () => setStep(prev => Math.min(prev + 1, 3));
    const handleBack = () => setStep(prev => Math.max(prev - 1, 0));

    const handleFileUpload = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = (evt) => {
            const bstr = evt.target.result;
            const wb = XLSX.read(bstr, { type: 'binary' });
            const wsname = wb.SheetNames[0];
            const ws = wb.Sheets[wsname];
            const data = XLSX.utils.sheet_to_json(ws);
            // Expecting columns 'Name' and 'Email'
            const guests = data.map(row => ({
                name: row.Name || row.name,
                email: row.Email || row.email
            })).filter(g => g.email);
            setFormData(prev => ({ ...prev, guests }));
        };
        reader.readAsBinaryString(file);
    };

    const handleSubmit = async () => {
        setLoading(true);
        try {
            // 1. Create Event
            const eventRes = await axios.post('http://localhost:5000/api/events', {
                title: formData.title,
                type: formData.type,
                date: formData.date,
                location: formData.location
            });

            const eventId = eventRes.data.id;

            // 2. Send Invitations
            await axios.post('http://localhost:5000/api/invitations', {
                event_id: eventId,
                guests: formData.guests
            });

            alert('Event created and invitations sent!');
            window.location.href = '/dashboard';
        } catch (err) {
            console.error(err);
            alert('Error creating event');
        } finally {
            setLoading(false);
        }
    };

    const stepNames = {
        en: ['Event Type', 'Details', 'Guests', 'Review'],
        he: ['סוג אירוע', 'פרטים', 'אורחים', 'סיכום']
    };

    const currentStepName = language === 'he' ? stepNames.he[step] : stepNames.en[step];

    return (
        <div className="split-view">
            <div className="wizard-container card">
                <h2>
                    {language === 'en' ? 'Create Event' : 'יצירת אירוע'} - {language === 'en' ? 'Step' : 'שלב'} {step + 1}: {currentStepName}
                </h2>

                <div className="wizard-content">
                    {step === 0 && (
                        <div className="event-type-selection">
                            <p style={{ textAlign: 'center', marginBottom: '2rem', fontSize: '1.1rem', color: 'var(--text-color)' }}>
                                {language === 'en' ? 'Select your event type' : 'בחר את סוג האירוע'}
                            </p>
                            <div className="event-type-grid">
                                {getAllEventTypes().map(eventType => (
                                    <div
                                        key={eventType}
                                        className={`event-type-card ${formData.type === eventType ? 'selected' : ''}`}
                                        onClick={() => setFormData({ ...formData, type: eventType })}
                                    >
                                        <div className="event-type-name-primary">{getEventTypeName(eventType, language)}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {step === 1 && (
                        <div className="form-step">
                            <label>{language === 'en' ? 'Event Title' : 'שם האירוע'}</label>
                            <input
                                value={formData.title}
                                onChange={e => setFormData({ ...formData, title: e.target.value })}
                                placeholder={language === 'en' ? "e.g. Yuval's Wedding" : "לדוגמה: החתונה של יובל"}
                            />
                            <label>{language === 'en' ? 'Type' : 'סוג'}</label>
                            <select value={formData.type} onChange={e => setFormData({ ...formData, type: e.target.value, background: '' })}>
                                {getAllEventTypes().map(eventType => (
                                    <option key={eventType} value={eventType}>
                                        {getEventTypeName(eventType, language)}
                                    </option>
                                ))}
                            </select>

                            <label>{language === 'en' ? 'Choose Background' : 'בחר רקע'}</label>
                            <div className="background-grid" style={{ marginTop: '10px' }}>
                                {getBackgrounds(formData.type).map((bg, index) => (
                                    <div
                                        key={bg}
                                        className={`bg-option ${formData.background === bg ? 'selected' : ''}`}
                                        onClick={() => setFormData({ ...formData, background: bg })}
                                        style={{
                                            backgroundImage: `url(${new URL(`../../background/${bg}`, import.meta.url).href})`,
                                            backgroundSize: 'cover',
                                            backgroundPosition: 'center',
                                            minHeight: '100px'
                                        }}
                                    >
                                        {!formData.background && index === 0 && <span style={{ background: 'rgba(255,255,255,0.8)', padding: '5px', borderRadius: '4px', fontSize: '0.8rem' }}>Default</span>}
                                    </div>
                                ))}
                            </div>

                            <label style={{ marginTop: '20px' }}>{language === 'en' ? 'Date' : 'תאריך'}</label>
                            <input
                                type="datetime-local"
                                value={formData.date}
                                onChange={e => setFormData({ ...formData, date: e.target.value })}
                            />
                            <label>{language === 'en' ? 'Location' : 'מיקום'}</label>
                            <input
                                value={formData.location}
                                onChange={e => setFormData({ ...formData, location: e.target.value })}
                            />
                        </div>
                    )}

                    {step === 2 && (
                        <div className="form-step">
                            <p>{language === 'en' ? 'Upload Excel file with columns: Name, Email' : 'העלה קובץ Excel עם עמודות: שם, אימייל'}</p>
                            <input type="file" accept=".xlsx, .xls" onChange={handleFileUpload} />
                            <p>{language === 'en' ? `Loaded ${formData.guests.length} guests` : `נטענו ${formData.guests.length} אורחים`}</p>
                            <ul>
                                {formData.guests.slice(0, 5).map((g, i) => <li key={i}>{g.name} - {g.email}</li>)}
                                {formData.guests.length > 5 && <li>{language === 'en' ? `...and ${formData.guests.length - 5} more` : `...ועוד ${formData.guests.length - 5}`}</li>}
                            </ul>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="review-step">
                            <h3>{language === 'en' ? 'Summary' : 'סיכום'}</h3>
                            <p><strong>{language === 'en' ? 'Event:' : 'אירוע:'}</strong> {formData.title}</p>
                            <p><strong>{language === 'en' ? 'Date:' : 'תאריך:'}</strong> {formData.date}</p>
                            <p><strong>{language === 'en' ? 'Guests:' : 'אורחים:'}</strong> {formData.guests.length}</p>
                            <button className="btn btn-primary" onClick={handleSubmit} disabled={loading}>
                                {loading ? (language === 'en' ? 'Sending...' : 'שולח...') : (language === 'en' ? 'Confirm & Send Invitations' : 'אשר ושלח הזמנות')}
                            </button>
                        </div>
                    )}
                </div>

                <div className="wizard-actions">
                    {step > 0 && <button className="btn" onClick={handleBack}>{language === 'en' ? 'Back' : 'חזור'}</button>}
                    {step < 3 && <button className="btn btn-primary" onClick={handleNext}>{language === 'en' ? 'Next' : 'הבא'}</button>}
                </div>
            </div>

            <div className="preview-wrapper">
                <h3>{language === 'en' ? 'Live Preview' : 'תצוגה מקדימה'}</h3>
                <EventPreview formData={formData} />
            </div>
        </div>
    );
}
