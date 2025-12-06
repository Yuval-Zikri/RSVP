import React from 'react';
import Modal from '../shared/Modal';

/**
 * Preview Modal Component - Displays email preview
 */
export default function PreviewModal({ isOpen, onClose, previewHtml, t }) {
    return (
        <Modal isOpen={isOpen} onClose={onClose} title={t.invitationPreview} size="large">
            <div className="preview-container">
                <iframe
                    srcDoc={previewHtml}
                    title="Email Preview"
                    style={{ width: '100%', height: '700px', border: 'none', borderRadius: '8px' }}
                />
            </div>
        </Modal>
    );
}
