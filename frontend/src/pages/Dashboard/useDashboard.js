import { useState, useEffect } from 'react';
import axios from 'axios';
import * as XLSX from 'xlsx';

export function useDashboard(t) {
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

    return {
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
    };
}
