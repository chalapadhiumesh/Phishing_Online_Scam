import React, { useContext } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { ThemeContext } from '../context/ThemeContext';
import { Shield, LayoutDashboard, Search, History, Moon, Sun, LogOut } from 'lucide-react';

const Layout = ({ children }) => {
  const { logout, user } = useContext(AuthContext);
  const { theme, toggleTheme } = useContext(ThemeContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-title">
          <Shield style={{ marginRight: '8px', verticalAlign: 'text-bottom' }} />
          ScamShield AI
        </div>
        
        <nav style={{ flex: 1 }}>
          <NavLink to="/dashboard" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>
            <LayoutDashboard size={20} />
            Dashboard
          </NavLink>
          <NavLink to="/scan/url" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>
            <Search size={20} />
            URL Scanner
          </NavLink>
          <NavLink to="/scan/message" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>
            <Search size={20} />
            Message Scanner
          </NavLink>
          <NavLink to="/history" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>
            <History size={20} />
            Scan History
          </NavLink>
        </nav>

        <div style={{ marginTop: 'auto' }}>
          <div style={{ marginBottom: '1rem', fontSize: '0.875rem' }}>
            User: {user?.username}
          </div>
          <button onClick={toggleTheme} className="nav-link" style={{ width: '100%', background: 'transparent', border: 'none', cursor: 'pointer', textAlign: 'left', color: 'var(--sidebar-text)' }}>
            {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
            Toggle Theme
          </button>
          <button onClick={handleLogout} className="nav-link" style={{ width: '100%', background: 'transparent', border: 'none', cursor: 'pointer', textAlign: 'left', color: '#ef4444' }}>
            <LogOut size={20} />
            Logout
          </button>
        </div>
      </aside>

      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

export default Layout;
