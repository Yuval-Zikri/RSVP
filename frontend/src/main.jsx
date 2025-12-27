import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles/theme.css'
import 'leaflet/dist/leaflet.css';
import axios from 'axios';

// Add ngrok-skip-browser-warning header to all requests
axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'true';

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
)
