import React, { useState } from 'react';
import axios from 'axios';
import { Shield, ShieldAlert, ShieldCheck, MessageSquare } from 'lucide-react';
import { getRiskColor, getRiskBackgroundColor } from '../utils/riskColors';

const MessageScanner = () => {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleScan = async (e) => {
    e.preventDefault();
    if (!message) return;
    
    setLoading(true);
    setError('');
    setResult(null);
    
    try {
      const res = await axios.post('/api/scan/message', { message });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during scanning. Please try again.');
    }
    setLoading(false);
  };

  const parseIndicators = (indicatorsStr) => {
    try {
      if (!indicatorsStr) return [];
      return typeof indicatorsStr === 'string' ? JSON.parse(indicatorsStr) : indicatorsStr;
    } catch (e) {
      return [];
    }
  };

  return (
    <div>
      <h1 className="card-title" style={{ fontSize: '1.5rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <MessageSquare size={24} color="var(--primary)" /> Message Scanner
      </h1>
      
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <p style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>Paste an SMS, email, or text message below to analyze it for scam patterns.</p>
        <form onSubmit={handleScan}>
          <textarea 
            className="form-input" 
            placeholder="Paste message content here..." 
            value={message} 
            onChange={e => setMessage(e.target.value)}
            required
            maxLength={10000}
            rows={5}
            style={{ width: '100%', marginBottom: '1rem', resize: 'vertical' }}
          />
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Scanning...' : 'Scan Message'}
          </button>
        </form>
        {error && <div style={{ marginTop: '1rem', color: 'var(--danger)' }}>{error}</div>}
      </div>

      {result && (
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
            {result.risk_level === 'HIGH' || result.risk_level === 'CRITICAL' ? (
              <ShieldAlert size={48} color={getRiskColor(result.risk_level)} />
            ) : result.risk_level === 'MEDIUM' ? (
              <Shield size={48} color={getRiskColor(result.risk_level)} />
            ) : (
              <ShieldCheck size={48} color={getRiskColor(result.risk_level)} />
            )}
            <div>
              <h2 style={{ fontSize: '1.25rem', marginBottom: '0.25rem' }}>Scan Result</h2>
              <div style={{ 
                display: 'inline-block', 
                padding: '0.25rem 0.75rem', 
                borderRadius: '9999px',
                fontSize: '0.875rem',
                fontWeight: 'bold',
                backgroundColor: getRiskBackgroundColor(result.risk_level),
                color: getRiskColor(result.risk_level)
              }}>
                {result.risk_level} RISK
              </div>
            </div>
          </div>
          
          <div style={{ marginBottom: '1.5rem' }}>
             <strong>Risk Score:</strong> <span>{result.risk_score}%</span>
          </div>

          {result.indicators && (
            <div>
              <h3 style={{ fontSize: '1rem', marginBottom: '0.75rem', color: 'var(--text-muted)' }}>Why this message was analyzed as {result.risk_level}:</h3>
              <ul style={{ listStyleType: 'disc', paddingLeft: '1.5rem', color: 'var(--text-main)' }}>
                {parseIndicators(result.indicators).map((indicator, idx) => (
                  <li key={idx} style={{ marginBottom: '0.5rem' }}>
                    {indicator}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default MessageScanner;