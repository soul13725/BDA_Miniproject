import React, { useState, useEffect } from 'react';
import { getLiveTransactions, getLiveStatus, startLiveStream, getCatalogFilters } from '../services/api';

export default function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const [filters, setFilters] = useState({
    categories: [],
    cities: ["Mumbai", "Pune", "Delhi", "Bengaluru", "Chennai", "Hyderabad"], // fallback if we don't fetch
    payments: ["Card", "UPI", "Wallet", "Cash"],
    channels: ["Online", "Store"]
  });

  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [cityFilter, setCityFilter] = useState('All');
  const [paymentFilter, setPaymentFilter] = useState('All');
  const [channelFilter, setChannelFilter] = useState('All');
  const [limit, setLimit] = useState(50);

  useEffect(() => {
    const init = async () => {
      try {
        const catFilters = await getCatalogFilters();
        setFilters(prev => ({ ...prev, categories: catFilters.categories }));
      } catch (err) {
        console.error(err);
      }
    };
    init();
  }, []);

  const fetchLive = async () => {
    try {
      const params = { limit };
      if (search) params.search = search;
      if (categoryFilter !== 'All') params.category = categoryFilter;
      if (cityFilter !== 'All') params.city = cityFilter;
      if (paymentFilter !== 'All') params.payment_method = paymentFilter;
      if (channelFilter !== 'All') params.channel = channelFilter;
      
      const [statusData, txnsData] = await Promise.all([
        getLiveStatus(),
        getLiveTransactions(params)
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
  }, [search, categoryFilter, cityFilter, paymentFilter, channelFilter, limit]);

  const handleStartStream = async () => {
    await startLiveStream();
    fetchLive();
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1400px' }}>
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
      
      <div className="card" style={{ marginBottom: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <input 
          type="text" 
          placeholder="Search by ID or Product..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ flex: 1, minWidth: '200px', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}
        />
        <select value={categoryFilter} onChange={(e) => setCategoryFilter(e.target.value)} style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
          <option value="All">All Categories</option>
          {filters.categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
        </select>
        <select value={cityFilter} onChange={(e) => setCityFilter(e.target.value)} style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
          <option value="All">All Cities</option>
          {filters.cities.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <select value={paymentFilter} onChange={(e) => setPaymentFilter(e.target.value)} style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
          <option value="All">All Payments</option>
          {filters.payments.map(p => <option key={p} value={p}>{p}</option>)}
        </select>
        <select value={channelFilter} onChange={(e) => setChannelFilter(e.target.value)} style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
          <option value="All">All Channels</option>
          {filters.channels.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <select value={limit} onChange={(e) => setLimit(Number(e.target.value))} style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
          <option value={50}>Last 50</option>
          <option value={100}>Last 100</option>
          <option value={500}>Last 500</option>
        </select>
      </div>
      
      <div className="card">
        {loading && transactions.length === 0 ? (
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
                {transactions.map(t => (
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
                      No live transactions available matching filters.<br/>
                      Wait for more stream data.
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
