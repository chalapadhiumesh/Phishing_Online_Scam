import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { History as HistoryIcon, ShieldAlert, ShieldCheck, Shield, Trash2, ChevronDown, ChevronUp } from 'lucide-react';
import { getRiskColor } from '../utils/riskColors';

const History = () => {
  const [activeTab, setActiveTab] = useState('urls');
  const [scans, setScans] = useState({ urls: [], messages: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [expandedId, setExpandedId] = useState(null);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      setError('');
      const [urlRes, msgRes] = await Promise.all([
        axios.get('/api/history/urls'),
        axios.get('/api/history/messages')
      ]);
      
      setScans({
        urls: urlRes.data.items || [],
        messages: msgRes.data.items || []
      });
    } catch (err) {
      console.error(err);
      setError('Unable to load scan history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const parseIndicators = (indicatorsStr) => {
    try {
      if (!indicatorsStr) return [];
      return typeof indicatorsStr === 'string' ? JSON.parse(indicatorsStr) : indicatorsStr;
    } catch (e) {
      return [];
    }
  };

  const handleDelete = async (id, type) => {
    if (!window.confirm('Are you sure you want to delete this scan record?')) return;
    try {
      await axios.delete(`/api/history/${type}/${id}`);
      fetchHistory();
    } catch (err) {
      alert('Failed to delete the record.');
    }
  };

  const handleDeleteAll = async () => {
    if (!window.confirm('Are you sure you want to delete all your scan history? This action cannot be undone.')) return;
    try {
      await axios.delete(`/api/history/${activeTab}`);
      fetchHistory();
    } catch (err) {
      alert('Failed to delete history.');
    }
  };

  const toggleExpand = (id) => {
    if (expandedId === id) setExpandedId(null);
    else setExpandedId(id);
  };

  const renderScanItem = (scan, type) => {
    const isExpanded = expandedId === scan.id;
    const indicators = parseIndicators(scan.indicators);

    return (
      <div key={scan.id} className="card" style={{ marginBottom: '1rem', transition: 'all 0.2s' }}>
        <div 
          style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}
          onClick={() => toggleExpand(scan.id)}
        >
          <div style={{ flex: 1, overflow: 'hidden', minWidth: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              {scan.risk_level === 'HIGH' || scan.risk_level === 'CRITICAL' ? (
                <ShieldAlert size={20} color={getRiskColor(scan.risk_level)} />
              ) : scan.risk_level === 'MEDIUM' ? (
                <Shield size={20} color={getRiskColor(scan.risk_level)} />
              ) : (
                <ShieldCheck size={20} color={getRiskColor(scan.risk_level)} />
              )}
              <strong style={{ color: getRiskColor(scan.risk_level) }}>
                {scan.risk_level} RISK
              </strong>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>• {formatDate(scan.timestamp)}</span>
            </div>
            <div style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', color: 'var(--text-main)', paddingRight: '1rem' }}>
              {type === 'urls' ? scan.url : scan.message_text}
            </div>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button 
              className="btn btn-danger" 
              style={{ padding: '0.5rem', borderRadius: '50%' }}
              onClick={(e) => { e.stopPropagation(); handleDelete(scan.id, type); }}
              title="Delete Record"
            >
              <Trash2 size={16} />
            </button>
            {isExpanded ? <ChevronUp size={20} color="var(--text-muted)" /> : <ChevronDown size={20} color="var(--text-muted)" />}
          </div>
        </div>

        {isExpanded && (
          <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border)' }}>
            <div style={{ marginBottom: '1rem' }}>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', display: 'block', marginBottom: '0.25rem' }}>
                {type === 'urls' ? 'Scanned URL' : 'Scanned Message'}
              </span>
              <div style={{ padding: '0.75rem', backgroundColor: 'var(--bg-color)', borderRadius: '0.5rem', wordBreak: 'break-word' }}>
                {type === 'urls' ? scan.url : scan.message_text}
              </div>
            </div>

            <div style={{ display: 'flex', gap: '2rem', marginBottom: '1rem' }}>
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', display: 'block' }}>Prediction</span>
                <strong style={{ textTransform: 'capitalize' }}>{scan.prediction}</strong>
              </div>
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', display: 'block' }}>Risk Score</span>
                <strong>{scan.risk_score}%</strong>
              </div>
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', display: 'block' }}>Confidence</span>
                <strong>{(scan.confidence * 100).toFixed(1)}%</strong>
              </div>
            </div>

            {indicators.length > 0 && (
              <div>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', display: 'block', marginBottom: '0.5rem' }}>Analysis Details</span>
                <ul style={{ listStyleType: 'disc', paddingLeft: '1.5rem', margin: 0 }}>
                  {indicators.map((ind, i) => (
                    <li key={i} style={{ marginBottom: '0.25rem' }}>{ind}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  const currentScans = activeTab === 'urls' ? scans.urls : scans.messages;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1 className="card-title" style={{ fontSize: '1.5rem', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <HistoryIcon size={24} color="var(--primary)" /> Scan History
        </h1>
        {currentScans.length > 0 && (
          <button className="btn btn-danger" onClick={handleDeleteAll}>
            Delete All History
          </button>
        )}
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem' }}>
        <button 
          className={`btn ${activeTab === 'urls' ? 'btn-primary' : 'btn-outline'}`}
          style={activeTab !== 'urls' ? { backgroundColor: 'transparent', color: 'var(--text-main)', border: '1px solid var(--border)' } : {}}
          onClick={() => { setActiveTab('urls'); setExpandedId(null); }}
        >
          URL Scans
        </button>
        <button 
          className={`btn ${activeTab === 'messages' ? 'btn-primary' : 'btn-outline'}`}
          style={activeTab !== 'messages' ? { backgroundColor: 'transparent', color: 'var(--text-main)', border: '1px solid var(--border)' } : {}}
          onClick={() => { setActiveTab('messages'); setExpandedId(null); }}
        >
          Message Scans
        </button>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <div className="spinner" style={{ marginBottom: '1rem' }}></div>
          <p style={{ color: 'var(--text-muted)' }}>Loading your history...</p>
        </div>
      ) : error ? (
        <div className="card text-center" style={{ padding: '3rem', border: '1px solid var(--danger)' }}>
          <ShieldAlert size={48} color="var(--danger)" style={{ marginBottom: '1rem', margin: '0 auto' }} />
          <p style={{ color: 'var(--danger)', fontWeight: 'bold' }}>{error}</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {currentScans.length === 0 ? (
            <div className="card text-center" style={{ padding: '4rem 2rem' }}>
              <HistoryIcon size={48} color="var(--text-muted)" style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>No scan history yet</h3>
              <p style={{ color: 'var(--text-muted)' }}>
                Your {activeTab === 'urls' ? 'URL' : 'message'} scans will appear here after you perform a scan.
              </p>
            </div>
          ) : (
            (currentScans || []).map(scan => renderScanItem(scan, activeTab))
          )}
        </div>
      )}
    </div>
  );
};

export default History;