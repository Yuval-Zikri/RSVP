import React, { useState, useContext } from 'react';
import axios from 'axios';
import { LanguageContext } from '../../contexts';
import EventPreview from '../../components/EventPreview';
import EventTypeSelector from '../../components/CreateEvent/EventTypeSelector';
import EventDetailsForm from '../../components/CreateEvent/EventDetailsForm';
import GuestManager from '../../components/CreateEvent/GuestManager';
import EventReview from '../../components/CreateEvent/EventReview';
import { getBackgrounds } from '../../utils/eventTypes';
import './CreateEvent.css';

export default function CreateEvent() {
    const context = useContext(LanguageContext);
    const language = context?.language || 'en';
    const [step, setStep] = useState(0);
    const [formData, setFormData] = useState({
        title: '',
        subtitle: '',
        type: 'wedding',
        background: '',
        date: '',
        location: '',
        address: '',
        latitude: null,
        longitude: null,
        guests: []
    });
    const [loading, setLoading] = useState(false);

    const handleNext = () => {
        if (step === 1) {
            if (!formData.title || !formData.date || !formData.location) {
                alert(language === 'en' ? 'Please fill in all required fields (Title, Date, Location)' : 'נא למלא את כל שדות החובה (שם, תאריך, מיקום)');
                return;
            }
        }
        setStep(prev => Math.min(prev + 1, 3));
    };

    const handleBack = () => setStep(prev => Math.max(prev - 1, 0));

    const handleSubmit = async () => {
        setLoading(true);
        try {
            // Create Event
            const eventRes = await axios.post('/api/events', {
                title: formData.title,
                subtitle: formData.subtitle,
                type: formData.type,
                date: formData.date,
                location: formData.location,
                address: formData.address,
                latitude: formData.latitude,
                longitude: formData.longitude,
                background_theme: formData.background || getBackgrounds(formData.type)[0],
                email_background_url: formData.background || getBackgrounds(formData.type)[0]
            });

            const eventId = eventRes.data.id;

            // Send Invitations
            await axios.post('/api/invitations', {
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
                        <EventTypeSelector
                            selectedType={formData.type}
                            onSelectType={(type) => setFormData({ ...formData, type })}
                            language={language}
                        />
                    )}

                    {step === 1 && (
                        <EventDetailsForm
                            formData={formData}
                            onFormDataChange={setFormData}
                            language={language}
                        />
                    )}

                    {step === 2 && (
                        <GuestManager
                            guests={formData.guests}
                            onAddGuests={(newGuests) => setFormData(prev => ({ ...prev, guests: [...prev.guests, ...newGuests] }))}
                            onRemoveGuest={(index) => setFormData(prev => ({ ...prev, guests: prev.guests.filter((_, i) => i !== index) }))}
                            language={language}
                        />
                    )}

                    {step === 3 && (
                        <EventReview
                            formData={formData}
                            onSubmit={handleSubmit}
                            loading={loading}
                            language={language}
                        />
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
