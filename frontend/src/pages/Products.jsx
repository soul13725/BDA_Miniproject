import React, { useState, useEffect } from 'react';
import { getLiveProducts } from '../services/api';

export default function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const [sortField, setSortField] = useState('revenue');
  const [sortOrder, setSortOrder] = useState('desc');
  const [categoryFilter, setCategoryFilter] = useState('All');

  const fetchProducts = async () => {
    try {
      const data = await getLiveProducts();
      setProducts(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
    const interval = setInterval(fetchProducts, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleSort = (field) => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('desc');
    }
  };

  const categories = ['All', ...new Set(products.map(p => p.category))];

  const filteredProducts = products.filter(p => {
    const matchesSearch = p.product_name.toLowerCase().includes(search.toLowerCase()) || p.product_id.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = categoryFilter === 'All' || p.category === categoryFilter;
    return matchesSearch && matchesCategory;
  }).sort((a, b) => {
    let valA = a[sortField];
    let valB = b[sortField];
    if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
    if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
    return 0;
  });

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px' }}>
      <h1 style={{ marginBottom: '0.2rem', color: 'var(--text-primary)' }}>RetailPulse Products</h1>
      <div style={{ fontSize: '1rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Live Product Analytics</div>
      <p style={{ marginBottom: '1.5rem', fontWeight: 600, color: 'var(--success)' }}>SOURCE: LIVE SIMULATED RETAIL DATA</p>
      
      <div className="card" style={{ marginBottom: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <input 
          type="text" 
          placeholder="Search products by ID or Name..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ flex: 1, minWidth: '200px', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)' }}
        />
        <select 
          value={categoryFilter} 
          onChange={(e) => setCategoryFilter(e.target.value)}
          style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      <div className="card">
        {loading ? (
          <div>Loading products...</div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid var(--border)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '0.75rem' }}>Product ID</th>
                <th style={{ padding: '0.75rem' }}>Name</th>
                <th style={{ padding: '0.75rem' }}>Category</th>
                <th style={{ padding: '0.75rem', cursor: 'pointer' }} onClick={() => handleSort('revenue')}>Live Revenue {sortField === 'revenue' ? (sortOrder === 'asc' ? '↑' : '↓') : ''}</th>
                <th style={{ padding: '0.75rem', cursor: 'pointer' }} onClick={() => handleSort('quantity')}>Live Quantity {sortField === 'quantity' ? (sortOrder === 'asc' ? '↑' : '↓') : ''}</th>
                <th style={{ padding: '0.75rem', cursor: 'pointer' }} onClick={() => handleSort('transaction_count')}>Transactions {sortField === 'transaction_count' ? (sortOrder === 'asc' ? '↑' : '↓') : ''}</th>
                <th style={{ padding: '0.75rem' }}>Avg Price</th>
              </tr>
            </thead>
            <tbody>
              {filteredProducts.map(p => (
                <tr key={p.product_id} style={{ borderBottom: '1px solid var(--border)' }}>
                  <td style={{ padding: '0.75rem', fontWeight: 600 }}>{p.product_id}</td>
                  <td style={{ padding: '0.75rem' }}>{p.product_name}</td>
                  <td style={{ padding: '0.75rem' }}>{p.category}</td>
                  <td style={{ padding: '0.75rem', color: 'var(--success)', fontWeight: 600 }}>₹{p.revenue.toLocaleString()}</td>
                  <td style={{ padding: '0.75rem' }}>{p.quantity}</td>
                  <td style={{ padding: '0.75rem' }}>{p.transaction_count}</td>
                  <td style={{ padding: '0.75rem' }}>₹{p.average_price.toLocaleString()}</td>
                </tr>
              ))}
              {products.length === 0 && (
                <tr>
                  <td colSpan="7" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>No live transactions available.<br/>Start the live stream to populate product analytics.</td>
                </tr>
              )}
              {products.length > 0 && filteredProducts.length === 0 && (
                 <tr>
                 <td colSpan="7" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>No products match your filters.</td>
               </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
