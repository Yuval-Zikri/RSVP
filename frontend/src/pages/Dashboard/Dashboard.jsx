import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import * as XLSX from 'xlsx';
import { LanguageContext } from '../../contexts';
import './Dashboard.css';

const translations = {
    en: {
        yourEvents: 'Your Events',
        noEvents: 'No events found.',
        dashboard: 'Dashboard',
        attending: 'Attending',
        totalPeople: 'Total People',
        pending: 'Pending',
        declined: 'Declined',
        guestList: 'Guest List',
        viewInvitation: 'View Invitation',
        remindAllPending: 'Remind All Pending',
        exportToExcel: 'Export to Excel',
        name: 'Name',
        status: 'Status',
        guests: 'Guests',
        total: 'Total',
        noGuests: 'No guests found for this event.',
        selectEvent: 'Select an event to view details',
        editEvent: 'Edit Event',
        deleteEvent: 'Delete Event',
        title: 'Title',
        subtitle: 'Subtitle',
        type: 'Type',
        dateTime: 'Date & Time',
        location: 'Location',
        cancel: 'Cancel',
        saveChanges: 'Save Changes',
        dateChangeWarning: '⚠️ Changing the date will reset all RSVPs and resend invitations!',
        invitationPreview: 'Invitation Preview',
        close: 'Close',
        deleteConfirm: 'Are you sure you want to delete this event?',
        failedToDelete: 'Failed to delete event',
        noPendingRsvps: 'No pending RSVPs to remind',
        sendRemindersConfirm: 'Send reminders to {count} pending guests?',
        failedToSend: 'Failed to send reminders',
        noDataToExport: 'No data to export',
        eventUpdated: 'Event updated successfully',
        dateChanged: 'Date changed! {count} invitation(s) have been resent and RSVPs reset.',
        failedToUpdate: 'Failed to update event',
        failedToLoadPreview: 'Failed to load preview',
        statusAttending: 'Attending',
        statusPending: 'Pending',
        statusNotAttending: 'Not Attending'
    },
    he: {
        yourEvents: 'האירועים שלך',
        noEvents: 'לא נמצאו אירועים.',
        dashboard: 'לוח בקרה',
        attending: 'מגיעים',
        totalPeople: 'סה״כ אנשים',
        pending: 'ממתינים',
        declined: 'לא מגיעים',
        guestList: 'רשימת מוזמנים',
        viewInvitation: 'צפייה בהזמנה',
        remindAllPending: 'שלח תזכורת לכולם',
        exportToExcel: 'ייצוא לאקסל',
        name: 'שם',
        status: 'סטטוס',
        guests: 'אורחים',
        total: 'סה״כ',
        noGuests: 'לא נמצאו אורחים לאירוע זה.',
        selectEvent: 'בחר אירוע כדי לצפות בפרטים',
        editEvent: 'ערוך אירוע',
        deleteEvent: 'מחק אירוע',
        title: 'כותרת',
        subtitle: 'כותרת משנה',
        type: 'סוג',
        dateTime: 'תאריך ושעה',
        location: 'מיקום',
        cancel: 'ביטול',
        saveChanges: 'שמור שינויים',
        dateChangeWarning: '⚠️ שינוי התאריך יאפס את כל התשובות וישלח הזמנות מחדש!',
        invitationPreview: 'תצוגה מקדימה של ההזמנה',
        close: 'סגור',
        deleteConfirm: 'האם אתה בטוח שברצונך למחוק את האירוע?',
        failedToDelete: 'נכשל במחיקת האירוע',
        noPendingRsvps: 'אין תשובות ממתינות',
        sendRemindersConfirm: 'לשלוח תזכורת ל-{count} אורחים ממתינים?',
        failedToSend: 'נכשל בשליחת תזכורות',
        noDataToExport: 'אין נתונים לייצוא',
        eventUpdated: 'האירוע עודכן בהצלחה',
        dateChanged: 'התאריך השתנה! {count} הזמנות נשלחו מחדש והתשובות אופסו.',
        failedToUpdate: 'נכשל בעדכון האירוע',
        failedToLoadPreview: 'נכשל בטעינת תצוגה מקדימה',
        statusAttending: 'מגיע',
        statusPending: 'ממתין',
        statusNotAttending: 'לא מגיע'
    }
};

export default function Dashboard() {
    const { language } = useContext(LanguageContext);
    const t = translations[language] || translations.en;

    const [events, setEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [rsvps, setRsvps] = useState([]);
    const [editModalOpen, setEditModalOpen] = useState(false);
    const [previewModalOpen, setPreviewModalOpen] = useState(false);
    const [previewHtml, setPreviewHtml] = useState('');
    const [editForm, setEditForm] = useState(null);

    useEffect(() => {
        fetchEvents();
    }, []);

    const fetchEvents = async () => {
        try {
            const res = await axios.get('/api/events');
            setEvents(res.data);
            if (selectedEvent) {
                const stillExists = res.data.find(e => e.id === selectedEvent.id);
                if (stillExists) {
                    setSelectedEvent(stillExists);
                } else {
                    setSelectedEvent(null);
                }
            }
        } catch (err) {
            console.error(err);
        }
    };

    const handleSelectEvent = async (event) => {
        setSelectedEvent(event);
        try {
            const res = await axios.get(`/api/events/${event.id}/rsvps`);
            setRsvps(res.data);
        } catch (err) {
            console.error("Failed to fetch RSVPs", err);
            setRsvps([]);
        }
    };

    const handleDeleteEvent = async (e, eventId) => {
        e.stopPropagation();
        if (window.confirm(t.deleteConfirm)) {
            try {
                await axios.delete(`/api/events/${eventId}`);
                fetchEvents();
                if (selectedEvent?.id === eventId) {
                    setSelectedEvent(null);
                    setRsvps([]);
                }
            } catch (err) {
                console.error("Failed to delete event", err);
                alert(t.failedToDelete);
            }
        }
    };

    const handleEditEvent = (e, event) => {
        e.stopPropagation();
        setEditForm({
            ...event,
            date: new Date(event.date).toISOString().slice(0, 16)
        });
        setEditModalOpen(true);
    };

    const handleSaveEdit = async () => {
        try {
            const response = await axios.put(`/api/events/${editForm.id}`, editForm);
            alert(response.data.message +
                (response.data.date_changed ?
                    `\n\n${t.dateChanged.replace('{count}', response.data.invitations_resent)}`
                    : ''));
            setEditModalOpen(false);
            fetchEvents();
            if (selectedEvent?.id === editForm.id) {
                const res = await axios.get(`/api/events/${editForm.id}/rsvps`);
                setRsvps(res.data);
            }
        } catch (err) {
            console.error("Failed to update event", err);
            alert(t.failedToUpdate + ': ' + (err.response?.data?.error || err.message));
        }
    };

    const handleRemindAll = async () => {
        const pendingRsvps = rsvps.filter(r => r.status === 'pending');
        if (pendingRsvps.length === 0) {
            alert(t.noPendingRsvps);
            return;
        }

        if (window.confirm(t.sendRemindersConfirm.replace('{count}', pendingRsvps.length))) {
            try {
                const response = await axios.post(`/api/events/${selectedEvent.id}/remind`);
                alert(response.data.message);
            } catch (err) {
                console.error("Failed to send reminders", err);
                alert(t.failedToSend);
            }
        }
    };

    const handleViewPreview = async () => {
        try {
            const response = await axios.get(`/api/events/${selectedEvent.id}/preview`);
            setPreviewHtml(response.data);
            setPreviewModalOpen(true);
        } catch (err) {
            console.error("Failed to load preview", err);
            alert(t.failedToLoadPreview);
        }
    };

    const handleExportToExcel = () => {
        if (rsvps.length === 0) {
            alert(t.noDataToExport);
            return;
        }

        const exportData = rsvps.map(r => ({
            Name: r.name,
            Email: r.email,
            Status: r.status,
            Guests: r.guests_count || 0,
            Total: r.status === 'attending' ? (1 + (r.guests_count || 0)) : 0
        }));

        const ws = XLSX.utils.json_to_sheet(exportData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Guest List");
        XLSX.writeFile(wb, `${selectedEvent.title}_guests.xlsx`);
    };

    return (
        <div className="dashboard-container" dir={language === 'he' ? 'rtl' : 'ltr'}>
            <div className="events-list card">
                <h3>{t.yourEvents}</h3>
                {events.length === 0 && <p>{t.noEvents}</p>}
                {events.map(ev => (
                    <div
                        key={ev.id}
                        className={`event-item ${selectedEvent?.id === ev.id ? 'active' : ''}`}
                        onClick={() => handleSelectEvent(ev)}
                    >
                        <div className="event-item-content">
                            <h4>{ev.title}</h4>
                            <p>{new Date(ev.date).toLocaleDateString()}</p>
                        </div>
                        <div className="event-item-actions">
                            <button
                                className="btn-edit"
                                onClick={(e) => handleEditEvent(e, ev)}
                                title={t.editEvent}
                            >
                                ✏️
                            </button>
                            <button
                                className="btn-delete"
                                onClick={(e) => handleDeleteEvent(e, ev)}
                                title={t.deleteEvent}
                            >
                                🗑️
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <div className="event-details card">
                {selectedEvent ? (
                    <>
                        <h3>{selectedEvent.title} - {t.dashboard}</h3>
                        <div className="stats-grid">
                            <div className="stat-box">
                                <span className="stat-value">{rsvps.filter(r => r.status === 'attending').length}</span>
                                <span className="stat-label">{t.attending}</span>
                            </div>
                            <div className="stat-box">
                                <span className="stat-value">
                                    {rsvps
                                        .filter(r => r.status === 'attending')
                                        .reduce((sum, r) => sum + 1 + (r.guests_count || 0), 0)
                                    }
                                </span>
                                <span className="stat-label">{t.totalPeople}</span>
                            </div>
                            <div className="stat-box">
                                <span className="stat-value">{rsvps.filter(r => r.status === 'pending').length}</span>
                                <span className="stat-label">{t.pending}</span>
                            </div>
                            <div className="stat-box">
                                <span className="stat-value">{rsvps.filter(r => r.status === 'not_attending').length}</span>
                                <span className="stat-label">{t.declined}</span>
                            </div>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                            <h4 style={{ margin: 0 }}>{t.guestList}</h4>
                            <div style={{ display: 'flex', gap: '10px' }}>
                                <button
                                    className="btn btn-info"
                                    onClick={handleViewPreview}
                                >
                                    👁️ {t.viewInvitation}
                                </button>
                                <button
                                    className="btn btn-secondary"
                                    onClick={handleRemindAll}
                                    disabled={rsvps.filter(r => r.status === 'pending').length === 0}
                                >
                                    📧 {t.remindAllPending}
                                </button>
                                <button
                                    className="btn btn-primary"
                                    onClick={handleExportToExcel}
                                    disabled={rsvps.length === 0}
                                >
                                    📊 {t.exportToExcel}
                                </button>
                            </div>
                        </div>
                        <div className="table-responsive">
                            <table className="rsvp-table">
                                <thead>
                                    <tr>
                                        <th>{t.name}</th>
                                        <th>{t.status}</th>
                                        <th>{t.guests}</th>
                                        <th>{t.total}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {rsvps.map((r, i) => (
                                        <tr key={i}>
                                            <td>{r.name} <span style={{ fontSize: '0.8em', color: '#666' }}>({r.email})</span></td>
                                            <td>
                                                <span className={`status-badge ${r.status}`}>
                                                    {r.status === 'attending' ? t.statusAttending :
                                                        r.status === 'pending' ? t.statusPending :
                                                            r.status === 'not_attending' ? t.statusNotAttending : r.status}
                                                </span>
                                            </td>
                                            <td>{r.guests_count}</td>
                                            <td>
                                                {r.status === 'attending' ? (1 + (r.guests_count || 0)) : '-'}
                                            </td>
                                        </tr>
                                    ))}
                                    {rsvps.length === 0 && (
                                        <tr>
                                            <td colSpan="4" style={{ textAlign: 'center' }}>{t.noGuests}</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </>
                ) : (
                    <p>{t.selectEvent}</p>
                )}
            </div>

            {/* Edit Modal */}
            {editModalOpen && (
                <div className="modal-overlay" onClick={() => setEditModalOpen(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <h2>{t.editEvent}</h2>
                        <div className="form-group">
                            <label>{t.title}</label>
                            <input
                                type="text"
                                value={editForm.title}
                                onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                            />
                        </div>
                        <div className="form-group">
                            <label>{t.subtitle}</label>
                            <input
                                type="text"
                                value={editForm.subtitle || ''}
                                onChange={(e) => setEditForm({ ...editForm, subtitle: e.target.value })}
                            />
                        </div>
                        <div className="form-group">
                            <label>{t.type}</label>
                            <input
                                type="text"
                                value={editForm.type}
                                onChange={(e) => setEditForm({ ...editForm, type: e.target.value })}
                            />
                        </div>
                        <div className="form-group">
                            <label>{t.dateTime}</label>
                            <input
                                type="datetime-local"
                                value={editForm.date}
                                onChange={(e) => setEditForm({ ...editForm, date: e.target.value })}
                            />
                            <small className="warning-text">{t.dateChangeWarning}</small>
                        </div>
                        <div className="form-group">
                            <label>{t.location}</label>
                            <input
                                type="text"
                                value={editForm.location}
                                onChange={(e) => setEditForm({ ...editForm, location: e.target.value })}
                            />
                        </div>
                        <div className="modal-actions">
                            <button className="btn btn-secondary" onClick={() => setEditModalOpen(false)}>{t.cancel}</button>
                            <button className="btn btn-primary" onClick={handleSaveEdit}>{t.saveChanges}</button>
                        </div>
                    </div>
                </div>
            )}

            {/* Preview Modal */}
            {previewModalOpen && (
                <div className="modal-overlay" onClick={() => setPreviewModalOpen(false)}>
                    <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                            <h2>{t.invitationPreview}</h2>
                            <button className="btn btn-secondary" onClick={() => setPreviewModalOpen(false)}>{t.close}</button>
                        </div>
                        <div className="preview-container">
                            <iframe
                                srcDoc={previewHtml}
                                title="Email Preview"
                                style={{ width: '100%', height: '700px', border: 'none', borderRadius: '8px' }}
                            />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
