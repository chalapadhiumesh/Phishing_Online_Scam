import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ShieldAlert, Shield, Link as LinkIcon, MessageSquare } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const renderCustomizedLabel = ({ x, y, cx, value }) => {
  if (value === 0) return null;
  // Offset the text horizontally from the end of the label line to create a clear gap
  const offset = x > cx ? 12 : -12;
  return (
    <text 
      x={x + offset} 
      y={y} 
      fill="var(--text-main)" 
      textAnchor={x > cx ? 'start' : 'end'} 
      dominantBaseline="central"
      fontSize={14}
      fontWeight="500"
    >
      {value}
    </text>
  );
};

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await axios.get('/api/dashboard/stats');
        setStats(res.data);
      } catch (err) {
        setError('Failed to load dashboard statistics.');
      }
      setLoading(false);
    };
    fetchStats();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;
  if (error) return <div style={{ color: 'var(--danger)' }}>{error}</div>;

  if (stats.total_scans === 0) {
    return (
      <div>
        <h1 className="card-title" style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Dashboard Overview</h1>
        <div className="card text-center" style={{ padding: '4rem 2rem' }}>
          <ShieldAlert size={64} color="var(--text-muted)" style={{ margin: '0 auto 1rem auto' }} />
          <h3>No scan data available yet</h3>
          <p style={{ color: 'var(--text-muted)' }}>Start scanning URLs or Messages to see your statistics here.</p>
        </div>
      </div>
    );
  }

  const urlData = [
    { name: 'Phishing', value: stats.url_scans.phishing, color: 'var(--danger)' },
    { name: 'Legitimate', value: stats.url_scans.legitimate, color: 'var(--success)' },
  ];

  const msgData = [
    { name: 'Scam', value: stats.message_scans.scam, color: 'var(--warning)' },
    { name: 'Legitimate', value: stats.message_scans.legitimate, color: 'var(--success)' },
  ];

  return (
    <div>
      <h1 className="card-title" style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Dashboard Overview</h1>
      
      <div className="dashboard-grid">
        <div className="card stat-card" style={{ marginBottom: 0 }}>
          <div className="stat-icon" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', color: 'var(--primary)' }}>
            <Shield size={24} />
          </div>
          <div className="stat-info">
            <h3>{stats.total_scans}</h3>
            <p>Total Scans</p>
          </div>
        </div>
        
        <div className="card stat-card" style={{ marginBottom: 0 }}>
          <div className="stat-icon" style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', color: 'var(--danger)' }}>
            <ShieldAlert size={24} />
          </div>
          <div className="stat-info">
            <h3 style={{ color: 'var(--danger)' }}>{stats.total_phishing}</h3>
            <p>Phishing/Scams</p>
          </div>
        </div>
        
        <div className="card stat-card" style={{ marginBottom: 0 }}>
          <div className="stat-icon" style={{ backgroundColor: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)' }}>
            <LinkIcon size={24} />
          </div>
          <div className="stat-info">
            <h3>{stats.url_scans.total}</h3>
            <p>URLs Scanned</p>
          </div>
        </div>
        
        <div className="card stat-card" style={{ marginBottom: 0 }}>
          <div className="stat-icon" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', color: 'var(--warning)' }}>
            <MessageSquare size={24} />
          </div>
          <div className="stat-info">
            <h3>{stats.message_scans.total}</h3>
            <p>Messages Scanned</p>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginTop: '1.5rem' }}>
        <div className="card">
          <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}><LinkIcon size={20}/> URL Scans</h3>
          {stats.url_scans.total > 0 ? (
            <div style={{ height: '300px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
                  <Pie 
                    data={urlData} 
                    dataKey="value" 
                    nameKey="name" 
                    cx="50%" 
                    cy="50%" 
                    outerRadius={80} 
                    labelLine={{ stroke: 'var(--text-muted)' }}
                    label={renderCustomizedLabel}
                  >
                    {urlData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p style={{ textAlign: 'center', color: 'var(--text-muted)' }}>No URL scans yet</p>
          )}
        </div>
        
        <div className="card">
          <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}><MessageSquare size={20}/> Message Scans</h3>
          {stats.message_scans.total > 0 ? (
            <div style={{ height: '300px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
                  <Pie 
                    data={msgData} 
                    dataKey="value" 
                    nameKey="name" 
                    cx="50%" 
                    cy="50%" 
                    outerRadius={80}
                    labelLine={{ stroke: 'var(--text-muted)' }}
                    label={renderCustomizedLabel}
                  >
                    {msgData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p style={{ textAlign: 'center', color: 'var(--text-muted)' }}>No message scans yet</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;