import React, { useContext } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { ShieldAlert, CheckCircle, Zap } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import { ThemeContext } from '../context/ThemeContext';

const Home = () => {
  const { user } = useContext(AuthContext);
  const { toggleTheme, theme } = useContext(ThemeContext);

  if (user) {
    return <Navigate to="/dashboard" />;
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '1.5rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border)' }}>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary)', display: 'flex', alignItems: 'center' }}>
          <ShieldAlert size={28} style={{ marginRight: '8px' }} />
          ScamShield AI
        </div>
        <nav style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button onClick={toggleTheme} className="btn" style={{ background: 'transparent', color: 'var(--text-main)', border: '1px solid var(--border)' }}>
            {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
          </button>
          <Link to="/login" className="btn" style={{ color: 'var(--text-main)' }}>Login</Link>
          <Link to="/register" className="btn btn-primary">Get Started</Link>
        </nav>
      </header>

      <main style={{ flex: 1, padding: '4rem 2rem', maxWidth: '1200px', margin: '0 auto', textAlign: 'center' }}>
        <h1 style={{ fontSize: '3.5rem', fontWeight: '800', marginBottom: '1.5rem', lineHeight: 1.2 }}>
          AI-Based Phishing & <br/><span style={{ color: 'var(--primary)' }}>Online Scam Intelligence</span>
        </h1>
        <p style={{ fontSize: '1.25rem', color: 'var(--text-muted)', marginBottom: '3rem', maxWidth: '800px', margin: '0 auto 3rem auto' }}>
          Protect yourself from cyber threats using advanced Machine Learning models. We analyze URLs and messages in real-time to detect phishing attempts and scams before they cause harm.
        </p>

        <div className="grid grid-cols-3" style={{ textAlign: 'left', marginTop: '4rem' }}>
          <div className="card">
            <div style={{ color: 'var(--primary)', marginBottom: '1rem' }}><ShieldAlert size={40} /></div>
            <h3>URL Phishing Detection</h3>
            <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>Our Random Forest and TF-IDF models inspect URL syntax and patterns to detect malicious websites with 99% accuracy.</p>
          </div>
          <div className="card">
            <div style={{ color: 'var(--success)', marginBottom: '1rem' }}><CheckCircle size={40} /></div>
            <h3>Scam Message Analysis</h3>
            <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>Advanced NLP determines the likelihood of SMS or email messages being fraudulent, highlighting suspicious keywords.</p>
          </div>
          <div className="card">
            <div style={{ color: 'var(--warning)', marginBottom: '1rem' }}><Zap size={40} /></div>
            <h3>Real-Time Analytics</h3>
            <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>Track your scan history, view detailed reports, and monitor personal threat intelligence statistics in your dashboard.</p>
          </div>
        </div>
      </main>
      
      <footer style={{ padding: '2rem', textAlign: 'center', borderTop: '1px solid var(--border)', color: 'var(--text-muted)' }}>
        <p>&copy; 2026 AI-Based Phishing & Online Scam Intelligence Platform. Final Year B.Tech Project.</p>
      </footer>
    </div>
  );
};

export default Home;
