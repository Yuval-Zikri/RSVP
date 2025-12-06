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
        setEditForm,
        setEditModalOpen,
        setPreviewModalOpen,
        handleSelectEvent,
        handleDeleteEvent,
        handleEditEvent,
        handleSaveEdit,
        handleRemindAll,
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
