import React from 'react';
import Modal from '../shared/Modal';

/**
 * Edit Event Modal Component
 */
export default function EditEventModal({
    isOpen,
    onClose,
    editForm,
    setEditForm,
    onSave,
    t
}) {
    if (!isOpen || !editForm) return null;

    return (
        <Modal isOpen={isOpen} onClose={onClose} title={t.editEvent} size="medium">
            <div className="form-group">
                <label>{t.title}</label>
                <input
                    type="text"
                    name="title"
                    value={editForm.title}
                    onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                />
            </div>
            <div className="form-group">
                <label>{t.subtitle}</label>
                <input
                    type="text"
                    name="subtitle"
                    value={editForm.subtitle || ''}
                    onChange={(e) => setEditForm({ ...editForm, subtitle: e.target.value })}
                />
            </div>
            <div className="form-group">
                <label>{t.type}</label>
                <input
                    type="text"
                    name="type"
                    value={editForm.type}
                    onChange={(e) => setEditForm({ ...editForm, type: e.target.value })}
                />
            </div>
            <div className="form-group">
                <label>{t.dateTime}</label>
                <input
                    type="datetime-local"
                    name="date"
                    value={editForm.date}
                    onChange={(e) => setEditForm({ ...editForm, date: e.target.value })}
                />
                <small className="warning-text">{t.dateChangeWarning}</small>
            </div>
            <div className="form-group">
                <label>{t.location}</label>
                <input
                    type="text"
                    name="location"
                    value={editForm.location}
                    onChange={(e) => setEditForm({ ...editForm, location: e.target.value })}
                />
            </div>
            <div className="modal-actions">
                <button className="btn btn-secondary" onClick={onClose}>{t.cancel}</button>
                <button className="btn btn-primary" onClick={onSave}>{t.saveChanges}</button>
            </div>
        </Modal>
    );
}
