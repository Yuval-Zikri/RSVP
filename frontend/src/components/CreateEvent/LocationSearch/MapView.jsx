import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

// Set up Leaflet default icon
let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Map marker component
function LocationMarker({ position, setPosition }) {
    const map = useMap();

    useEffect(() => {
        map.invalidateSize();
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

// Stable constants to prevent re-renders
const MAP_CENTER = [32.0853, 34.7818];
const MAP_STYLE = { height: '100%', width: '100%' };
const CONTAINER_STYLE = { height: '300px', width: '100%', borderRadius: '8px', overflow: 'hidden', border: '1px solid #ccc' };

/**
 * Map View Component - Interactive map with marker
 */
const MapView = React.memo(({
    latitude,
    longitude,
    onLocationSelect,
    onSearchQueryChange,
    language
}) => {
    const setMapPosition = React.useCallback(async (latlng) => {
        // Update parent with just the location coordinates first
        onLocationSelect({
            latitude: latlng.lat,
            longitude: latlng.lng
        });

        // Reverse Geocoding
        try {
            const response = await axios.get(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latlng.lat}&lon=${latlng.lng}&accept-language=he`);
            if (response.data && response.data.display_name) {
                const address = response.data.display_name;
                onSearchQueryChange(address);
                onLocationSelect({
                    location: address.split(',')[0],
                    address: address,
                    latitude: latlng.lat,
                    longitude: latlng.lng
                });
            }
        } catch (error) {
            console.error("Reverse geocoding failed", error);
        }
    }, [onLocationSelect, onSearchQueryChange]);

    // Component to handle map resizing
    function MapInvalidator() {
        const map = useMap();
        useEffect(() => {
            map.invalidateSize();
            // multiple invalidations to catch different render timing
            const t1 = setTimeout(() => map.invalidateSize(), 100);
            const t2 = setTimeout(() => map.invalidateSize(), 500);
            return () => { clearTimeout(t1); clearTimeout(t2); };
        }, [map]);
        return null;
    }

    const markerPosition = React.useMemo(() => {
        return latitude != null && longitude != null
            ? { lat: latitude, lng: longitude }
            : null;
    }, [latitude, longitude]);

    return (
        <>
            <div className="map-container" style={CONTAINER_STYLE}>
                <MapContainer center={MAP_CENTER} zoom={13} style={MAP_STYLE}>
                    <MapInvalidator />
                    <TileLayer
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    />
                    <LocationMarker
                        position={markerPosition}
                        setPosition={setMapPosition}
                    />
                </MapContainer>
            </div>
            <p style={{ fontSize: '0.8rem', color: '#666', marginTop: '5px' }}>
                {language === 'en' ? '* Click on the map or drag the marker to adjust location' : '* לחץ על המפה או גרור את הסמן כדי לדייק את המיקום'}
            </p>
        </>
    );
});

export default MapView;
