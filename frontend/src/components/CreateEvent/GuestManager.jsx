import React, { useState } from 'react';
import * as XLSX from 'xlsx';

/**
 * Guest Manager Component (Step 2 of Create Event)
 * Handles both Excel import and manual addition of guests
 */
export default function GuestManager({ guests, onAddGuests, onRemoveGuest, language }) {
    const [activeTab, setActiveTab] = useState('import');
    const [manualEntry, setManualEntry] = useState({ name: '', email: '' });

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
            const newGuests = data.map(row => ({
                name: row.Name || row.name,
                email: row.Email || row.email
            })).filter(g => g.email);
            onAddGuests(newGuests);
        };
        reader.readAsBinaryString(file);
    };

    const handleManualAdd = () => {
        if (manualEntry.name && manualEntry.email) {
            onAddGuests([manualEntry]);
            setManualEntry({ name: '', email: '' });
        }
    };

    const downloadSample = (e) => {
        e.preventDefault();
        const ws = XLSX.utils.json_to_sheet([{ Name: 'John Doe', Email: 'john@example.com' }]);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Guests");
        XLSX.writeFile(wb, "guests_sample.xlsx");
    };

    return (
        <div className="form-step">
            <div className="guest-import-tabs">
                <button
                    className={`tab-btn ${activeTab === 'import' ? 'active' : ''}`}
                    onClick={() => setActiveTab('import')}
                >
                    {language === 'en' ? 'Import Excel' : 'ייבוא מאקסל'}
                </button>
                <button
                    className={`tab-btn ${activeTab === 'manual' ? 'active' : ''}`}
                    onClick={() => setActiveTab('manual')}
                >
                    {language === 'en' ? 'Manual Add' : 'הוספה ידנית'}
                </button>
            </div>

            <div className="tab-content">
                {activeTab === 'import' && (
                    <div className="import-section">
                        <div className="sample-download">
                            <a href="#" onClick={downloadSample}>
                                {language === 'en' ? 'Download sample file - Click here' : 'להורדת קובץ לדוגמה - לחצו כאן'}
                            </a>
                        </div>

                        <div className="file-upload-container">
                            <label>{language === 'en' ? 'Upload File' : 'העלאת קובץ'}</label>
                            <div className="file-input-wrapper">
                                <input
                                    type="file"
                                    accept=".xlsx, .xls, .csv"
                                    onChange={handleFileUpload}
                                    id="file-upload"
                                    className="file-input"
                                />
                                <label htmlFor="file-upload" className="btn btn-secondary">
                                    {language === 'en' ? 'Choose File' : 'בחירת קובץ'}
                                </label>
                                <span className="file-name">
                                    {language === 'en' ? '* Select .xlsx or .csv file only' : '* נא לבחור קובץ (סיומת xls או csv בלבד)'}
                                </span>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'manual' && (
                    <div className="manual-add-section">
                        <div className="manual-input-group">
                            <input
                                placeholder={language === 'en' ? 'Name' : 'שם מלא'}
                                value={manualEntry.name}
                                onChange={e => setManualEntry({ ...manualEntry, name: e.target.value })}
                            />
                            <input
                                placeholder={language === 'en' ? 'Email' : 'אימייל'}
                                value={manualEntry.email}
                                onChange={e => setManualEntry({ ...manualEntry, email: e.target.value })}
                            />
                            <button
                                className="btn btn-success"
                                onClick={handleManualAdd}
                                disabled={!manualEntry.name || !manualEntry.email}
                            >
                                {language === 'en' ? 'Add' : 'הוסף'}
                            </button>
                        </div>
                    </div>
                )}
            </div>

            <div className="guests-list-summary">
                <h4>{language === 'en' ? `Guests List (${guests.length})` : `רשימת אורחים (${guests.length})`}</h4>
                <div className="guests-scroll-list">
                    {guests.map((g, i) => (
                        <div key={i} className="guest-item">
                            <span>{g.name} ({g.email})</span>
                            <button
                                className="remove-guest-btn"
                                onClick={() => onRemoveGuest(i)}
                                title={language === 'en' ? 'Remove' : 'הסר'}
                            >
                                ×
                            </button>
                        </div>
                    ))}
                    {guests.length === 0 && (
                        <p className="no-guests">{language === 'en' ? 'No guests added yet' : 'טרם נוספו אורחים'}</p>
                    )}
                </div>
            </div>
        </div>
    );
}
