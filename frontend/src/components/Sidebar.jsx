import React, { useContext } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ThemeContext, LanguageContext } from '../contexts';
import '../styles/theme.css';

const Sidebar = () => {
    const { theme, toggleTheme } = useContext(ThemeContext);
    const { language, setLanguage } = useContext(LanguageContext);
    const location = useLocation();

    const toggleLanguage = () => {
        setLanguage(prev => prev === 'en' ? 'he' : 'en');
    };

    const navItems = [
        { path: '/', label: language === 'en' ? 'Create Event' : 'יצירת אירוע', icon: '✨' },
        { path: '/dashboard', label: language === 'en' ? 'Dashboard' : 'לוח בקרה', icon: '📊' },
    ];

    return (
        <div className={`sidebar ${language === 'he' ? 'rtl' : 'ltr'}`}>
            <div className="sidebar-header">
                <h2>{language === 'en' ? 'EventMgr' : 'ניהול אירועים'}</h2>
            </div>

            <nav className="sidebar-nav">
                {navItems.map(item => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
                    >
                        <span className="icon">{item.icon}</span>
                        <span className="label">{item.label}</span>
                    </Link>
                ))}
            </nav>

            <div className="sidebar-footer">
                <button onClick={toggleTheme} className="icon-btn" title="Toggle Theme">
                    {theme === 'light' ? '🌙' : '☀️'}
                </button>
                <button onClick={toggleLanguage} className="icon-btn" title="Switch Language">
                    {language === 'en' ? '🇮🇱' : '🇺🇸'}
                </button>
            </div>
        </div>
    );
};

export default Sidebar;
