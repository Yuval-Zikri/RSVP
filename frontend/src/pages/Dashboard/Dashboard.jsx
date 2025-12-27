import React, { useContext } from 'react';
import { LanguageContext } from '../../contexts';
import EventsList from '../../components/Dashboard/EventsList';
import EventStatistics from '../../components/Dashboard/EventStatistics';
import GuestTable from '../../components/Dashboard/GuestTable';
import EditEventModal from '../../components/Dashboard/EditEventModal';
import PreviewModal from '../../components/Dashboard/PreviewModal';
import { dashboardTranslations } from './dashboardTranslations';
import { useDashboard } from './useDashboard';
import './Dashboard.css';

export default function Dashboard() {
    const { language } = useContext(LanguageContext);
    const t = dashboardTranslations[language] || dashboardTranslations.en;

    const {
        events,
        selectedEvent,
        rsvps,
        editModalOpen,
        previewModalOpen,
        previewHtml,
        editForm,
        newGuest,
        setEditForm,
        setEditModalOpen,
        setPreviewModalOpen,
        setNewGuest,
        handleSelectEvent,
        handleDeleteEvent,
        handleDeleteAllEvents,
        handleEditEvent,
        handleSaveEdit,
        handleRemindAll,
        handleAddGuest,
        handleViewPreview,
        handleExportToExcel
    } = useDashboard(t);

    return (
        <div className="dashboard-container" dir={language === 'he' ? 'rtl' : 'ltr'}>
            <EventsList
                events={events}
                selectedEvent={selectedEvent}
                onSelectEvent={handleSelectEvent}
                onEditEvent={handleEditEvent}
                onDeleteEvent={handleDeleteEvent}
                onDeleteAllEvents={handleDeleteAllEvents}
                t={t}
            />

            <div className="event-details card">
                {selectedEvent ? (
                    <>
                        <h3>{selectedEvent.title} - {t.dashboard}</h3>

                        <EventStatistics rsvps={rsvps} t={t} />

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                            <h4 style={{ margin: 0 }}>{t.guestList}</h4>
                            <div style={{ display: 'flex', gap: '10px' }}>
                                <button className="btn btn-info" onClick={handleViewPreview}>
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

                        <GuestTable rsvps={rsvps} t={t} />

                        <div className="add-guest-section">
                            <h4>{t.addGuest}</h4>
                            <form className="add-guest-form" onSubmit={handleAddGuest}>
                                <div className="form-group">
                                    <label>{t.name}</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={newGuest.name}
                                        onChange={(e) => setNewGuest({ ...newGuest, name: e.target.value })}
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>{t.email}</label>
                                    <input
                                        type="email"
                                        className="form-control"
                                        value={newGuest.email}
                                        onChange={(e) => setNewGuest({ ...newGuest, email: e.target.value })}
                                        required
                                    />
                                </div>
                                <button type="submit" className="btn btn-primary">
                                    ➕ {t.add}
                                </button>
                            </form>
                        </div>
                    </>
                ) : (
                    <p>{t.selectEvent}</p>
                )}
            </div>

            <EditEventModal
                isOpen={editModalOpen}
                onClose={() => setEditModalOpen(false)}
                editForm={editForm}
                setEditForm={setEditForm}
                onSave={handleSaveEdit}
                t={t}
            />

            <PreviewModal
                isOpen={previewModalOpen}
                onClose={() => setPreviewModalOpen(false)}
                previewHtml={previewHtml}
                t={t}
            />
        </div>
    );
}
