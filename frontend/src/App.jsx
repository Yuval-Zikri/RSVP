import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/theme.css';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard/Dashboard';
import RSVP from './pages/RSVP/RSVP';
import { ThemeContext, LanguageContext } from './contexts';
import ErrorBoundary from './components/ErrorBoundary';

const CreateEvent = React.lazy(() => import('./pages/CreateEvent/CreateEvent'));

function App() {
  const [theme, setTheme] = useState(window.location.pathname.startsWith('/rsvp') ? 'dark' : 'light');
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
          <ErrorBoundary>
            <AppContent />
          </ErrorBoundary>
        </Router>
      </LanguageContext.Provider>
    </ThemeContext.Provider>
  );
}

function AppContent() {
  const { language } = React.useContext(LanguageContext);
  const isRSVP = window.location.pathname.startsWith('/rsvp');

  return (
    <div className={`app-container ${language === 'he' ? 'layout-rtl' : 'layout-ltr'}`}>
      {!isRSVP && <Sidebar />}

      <main className="main-content" style={isRSVP ? { padding: 0, width: '100%' } : {}}>
        <React.Suspense fallback={<div>Loading...</div>}>
          <Routes>
            <Route path="/" element={<CreateEvent />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/rsvp/:token" element={<RSVP />} />
          </Routes>
        </React.Suspense>
      </main>
    </div>
  );
}

export default App;
