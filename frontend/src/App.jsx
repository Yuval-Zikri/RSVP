import React, { useState, useEffect, createContext } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/theme.css';
import Sidebar from './components/Sidebar';
import CreateEvent from './pages/CreateEvent/CreateEvent';
import Dashboard from './pages/Dashboard/Dashboard';
import RSVP from './pages/RSVP/RSVP';

export const ThemeContext = createContext();
export const LanguageContext = createContext();

function App() {
  const [theme, setTheme] = useState('light');
  const [language, setLanguage] = useState('en'); // 'en' or 'he'

  useEffect(() => {
    document.body.setAttribute('data-theme', theme);
    document.body.setAttribute('dir', language === 'he' ? 'rtl' : 'ltr');
  }, [theme, language]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <LanguageContext.Provider value={{ language, setLanguage }}>
        <Router>
          <AppContent />
        </Router>
      </LanguageContext.Provider>
    </ThemeContext.Provider>
  );
}

function AppContent() {
  const { language } = React.useContext(LanguageContext);
  const location = window.location;
  // Check if current path is RSVP page
  const isRSVP = window.location.pathname.startsWith('/rsvp');

  return (
    <div className={`app-container ${language === 'he' ? 'layout-rtl' : 'layout-ltr'}`}>
      {!isRSVP && <Sidebar />}

      <main className="main-content" style={isRSVP ? { padding: 0, width: '100%' } : {}}>
        <Routes>
          <Route path="/" element={<CreateEvent />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/rsvp/:token" element={<RSVP />} />
        </Routes>
      </main>
    </div>
  );
}


export default App;
