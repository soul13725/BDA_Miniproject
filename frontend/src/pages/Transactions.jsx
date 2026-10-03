import React, { useState, useEffect } from 'react';
import { getLiveTransactions, getLiveStatus, startLiveStream } from '../services/api';

export default function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchLive = async () => {
    try {
      const [statusData, txnsData] = await Promise.all([
        getLiveStatus(),
        getLiveTransactions(50)
      ]);
      setStatus(statusData);
      setTransactions(txnsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLive();
    const interval = setInterval(fetchLive, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleStartStream = async () => {
    await startLiveStream();
    fetchLive();
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem', alignItems: 'flex-start' }}>
        <div>
          <h1 style={{ color: 'var(--text-primary)', marginBottom: '0.2rem' }}>RetailPulse Transactions</h1>
          <div style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>Live Transaction Stream</div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span style={{ 
            padding: '0.25rem 0.5rem', 
            borderRadius: '4px', 
            background: status?.is_running ? 'var(--success)' : 'var(--muted)', 
            color: '#fff',
            fontWeight: 'bold',
            fontSize: '0.8rem'
          }}>
            {status?.is_running ? '● LIVE' : '○ OFFLINE'}
          </span>
          {!status?.is_running && (
            <button onClick={handleStartStream} style={{ padding: '0.5rem 1rem', background: 'var(--primary)', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
              Start Stream
            </button>
          )}
        </div>
      </header>
      
      <div className="card">
        {loading ? (
          <div>Loading transactions...</div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid var(--border)', color: 'var(--text-muted)' }}>
                  <th style={{ padding: '0.75rem' }}>Transaction ID</th>
                  <th style={{ padding: '0.75rem' }}>Timestamp</th>
                  <th style={{ padding: '0.75rem' }}>Customer</th>
                  <th style={{ padding: '0.75rem' }}>Product</th>
                  <th style={{ padding: '0.75rem' }}>Category</th>
                  <th style={{ padding: '0.75rem' }}>Qty</th>
                  <th style={{ padding: '0.75rem' }}>Total Amount</th>
                  <th style={{ padding: '0.75rem' }}>Payment</th>
                  <th style={{ padding: '0.75rem' }}>City</th>
                  <th style={{ padding: '0.75rem' }}>Channel</th>
                </tr>
              </thead>
              <tbody>
                {[...transactions].reverse().map(t => (
                  <tr key={t.transaction_id} style={{ borderBottom: '1px solid var(--border)' }}>
                    <td style={{ padding: '0.75rem', fontWeight: 500 }}>{t.transaction_id}</td>
                    <td style={{ padding: '0.75rem', color: 'var(--text-muted)' }}>{t.timestamp}</td>
                    <td style={{ padding: '0.75rem' }}>{t.customer_id}</td>
                    <td style={{ padding: '0.75rem' }}>{t.product_name}</td>
                    <td style={{ padding: '0.75rem' }}>{t.category}</td>
                    <td style={{ padding: '0.75rem' }}>{t.quantity}</td>
                    <td style={{ padding: '0.75rem', fontWeight: 'bold' }}>₹{t.total_amount}</td>
                    <td style={{ padding: '0.75rem' }}>{t.payment_method}</td>
                    <td style={{ padding: '0.75rem' }}>{t.city}</td>
                    <td style={{ padding: '0.75rem' }}>{t.channel}</td>
                  </tr>
                ))}
                {transactions.length === 0 && (
                  <tr>
                    <td colSpan="10" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                      No live transactions available.<br/>
                      Start the live stream to begin collecting data.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
