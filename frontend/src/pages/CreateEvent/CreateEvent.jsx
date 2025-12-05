import React, { useState, useContext, useEffect } from 'react';
import * as XLSX from 'xlsx';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, useMapEvents, useMap } from 'react-leaflet';
import { OpenStreetMapProvider } from 'leaflet-geosearch';
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import './CreateEvent.css';
import EventPreview from '../../components/EventPreview';
import { LanguageContext } from '../../contexts';
import EVENT_TYPES, { getAllEventTypes, getEventTypeName, getBackgrounds, getEmailBackground } from '../../utils/eventTypes';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

function LocationMarker({ position, setPosition }) {
    const map = useMap();

    useEffect(() => {
        if (position) {
            map.flyTo(position, 13);
        }
    }, [position, map]);

    useMapEvents({
        click(e) {
            setPosition(e.latlng);
        },
    });

    return position ? (
        <Marker
            position={position}
            draggable={true}
            eventHandlers={{
                dragend: (e) => setPosition(e.target.getLatLng())
            }}
        />
    ) : null;
}

export default function CreateEvent() {
    const context = useContext(LanguageContext);
    const language = context?.language || 'en'; // Default to 'en' if context is not available
    const [step, setStep] = useState(0);
    const [formData, setFormData] = useState({
        title: '',
        subtitle: '',
        type: 'wedding',
        background: '', // Selected background image
        date: '',
        location: '',
        address: '',
        latitude: null,
        longitude: null,
        guests: [] // Array of {name, email}
    });
    const [searchResults, setSearchResults] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [activeTab, setActiveTab] = useState('import');
    const [manualEntry, setManualEntry] = useState({ name: '', email: '' });

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

    const handleManualAdd = () => {
        if (manualEntry.name && manualEntry.email) {
            setFormData(prev => ({
                ...prev,
                guests: [...prev.guests, manualEntry]
            }));
            setManualEntry({ name: '', email: '' });
        }
    };

    const removeGuest = (index) => {
        setFormData(prev => ({
            ...prev,
            guests: prev.guests.filter((_, i) => i !== index)
        }));
    };

    const handleSearch = async () => {
        if (!searchQuery) return;
        setLoading(true);

        try {
            // 1. OpenStreetMap Search
            const provider = new OpenStreetMapProvider({
                params: {
                    'accept-language': 'he',
                    countrycodes: 'il',
                    addressdetails: 1,
                },
            });

            const osmPromise = provider.search({ query: searchQuery })
                .catch(err => {
                    console.error("OSM search failed", err);
                    return [];
                });

            // 2. Waze Search (via Backend)
            const wazePromise = axios.get(`/api/search-location?q=${encodeURIComponent(searchQuery)}`)
                .then(res => res.data || [])
                .catch(err => {
                    console.error("Waze search failed", err);
                    return [];
                });

            // Run both in parallel
            const [osmResults, wazeResults] = await Promise.all([osmPromise, wazePromise]);

            // Combine results (Waze first as it might be more relevant for local places)
            // Filter out duplicates based on label
            const allResults = [...wazeResults, ...osmResults];
            const uniqueResults = Array.from(new Map(allResults.map(item => [item.label, item])).values());

            setSearchResults(uniqueResults);
        } catch (error) {
            console.error("Search failed", error);
        } finally {
            setLoading(false);
        }
    };

    const selectLocation = (result) => {
        setFormData(prev => ({
            ...prev,
            location: result.label.split(',')[0],
            address: result.label,
            latitude: result.y,
            longitude: result.x
        }));
        setSearchResults([]);
        setSearchQuery(result.label);
    };

    const setMapPosition = async (latlng) => {
        setFormData(prev => ({
            ...prev,
            latitude: latlng.lat,
            longitude: latlng.lng
        }));

        // Reverse Geocoding
        try {
            const response = await axios.get(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latlng.lat}&lon=${latlng.lng}&accept-language=he`);
            if (response.data && response.data.display_name) {
                const address = response.data.display_name;
                setSearchQuery(address);
                setFormData(prev => ({
                    ...prev,
                    location: address.split(',')[0], // Try to get a short name
                    address: address
                }));
            }
        } catch (error) {
            console.error("Reverse geocoding failed", error);
        }
    };

    const handleSubmit = async () => {
        setLoading(true);
        try {
            // 1. Create Event
            const eventRes = await axios.post('/api/events', {
                title: formData.title,
                subtitle: formData.subtitle,
                type: formData.type,
                date: formData.date,
                location: formData.location,
                address: formData.address,
                latitude: formData.latitude,
                longitude: formData.longitude,
                background_theme: formData.background || getBackgrounds(formData.type)[0], // Local filename
                email_background_url: formData.background || getBackgrounds(formData.type)[0] // Send filename, backend will construct URL
            });

            const eventId = eventRes.data.id;

            // 2. Send Invitations
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
                            <label>{language === 'en' ? 'Subtitle / Hosts' : 'תת כותרת / מארחים'}</label>
                            <input
                                value={formData.subtitle}
                                onChange={e => setFormData({ ...formData, subtitle: e.target.value })}
                                placeholder={language === 'en' ? "e.g. Hila & Ido" : "לדוגמה: הילה & עידו"}
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
                                min={new Date().toISOString().slice(0, 16)}
                            />
                            <label>{language === 'en' ? 'Location Search' : 'חיפוש מיקום'}</label>
                            <div className="location-search-container">
                                <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
                                    <input
                                        value={searchQuery}
                                        onChange={e => setSearchQuery(e.target.value)}
                                        placeholder={language === 'en' ? 'Search for a place...' : 'חפש כתובת או מקום...'}
                                        style={{ flex: 1 }}
                                        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                                    />
                                    <button className="btn btn-secondary" onClick={handleSearch}>
                                        🔍
                                    </button>
                                </div>

                                {searchResults.length > 0 && (
                                    <ul className="search-results-list">
                                        {searchResults.map((result, idx) => (
                                            <li key={idx} onClick={() => selectLocation(result)}>
                                                {result.label}
                                            </li>
                                        ))}
                                    </ul>
                                )}

                                <div className="map-container" style={{ height: '300px', width: '100%', borderRadius: '8px', overflow: 'hidden', border: '1px solid #ccc' }}>
                                    <MapContainer center={[32.0853, 34.7818]} zoom={13} style={{ height: '100%', width: '100%' }}>
                                        <TileLayer
                                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                        />
                                        <LocationMarker
                                            position={formData.latitude && formData.longitude ? { lat: formData.latitude, lng: formData.longitude } : null}
                                            setPosition={setMapPosition}
                                        />
                                    </MapContainer>
                                </div>
                                <p style={{ fontSize: '0.8rem', color: '#666', marginTop: '5px' }}>
                                    {language === 'en' ? '* Click on the map or drag the marker to adjust location' : '* לחץ על המפה או גרור את הסמן כדי לדייק את המיקום'}
                                </p>
                            </div>
                        </div>
                    )}

                    {step === 2 && (
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
                                            <a href="#" onClick={(e) => {
                                                e.preventDefault();
                                                const ws = XLSX.utils.json_to_sheet([{ Name: 'John Doe', Email: 'john@example.com' }]);
                                                const wb = XLSX.utils.book_new();
                                                XLSX.utils.book_append_sheet(wb, ws, "Guests");
                                                XLSX.writeFile(wb, "guests_sample.xlsx");
                                            }}>
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
                                <h4>{language === 'en' ? `Guests List (${formData.guests.length})` : `רשימת אורחים (${formData.guests.length})`}</h4>
                                <div className="guests-scroll-list">
                                    {formData.guests.map((g, i) => (
                                        <div key={i} className="guest-item">
                                            <span>{g.name} ({g.email})</span>
                                            <button
                                                className="remove-guest-btn"
                                                onClick={() => removeGuest(i)}
                                                title={language === 'en' ? 'Remove' : 'הסר'}
                                            >
                                                ×
                                            </button>
                                        </div>
                                    ))}
                                    {formData.guests.length === 0 && (
                                        <p className="no-guests">{language === 'en' ? 'No guests added yet' : 'טרם נוספו אורחים'}</p>
                                    )}
                                </div>
                            </div>
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
