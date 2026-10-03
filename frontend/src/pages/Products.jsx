import React, { useState, useEffect } from 'react';
import { getCatalogProducts, getCatalogFilters } from '../services/api';

export default function Products() {
  const [products, setProducts] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const [page, setPage] = useState(1);
  const pageSize = 50;
  
  const [sortField, setSortField] = useState('revenue');
  const [sortOrder, setSortOrder] = useState('desc');
  
  const [filters, setFilters] = useState({
    categories: [],
    subcategories: [],
    product_classes: [],
    brands: []
  });
  
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [subcategoryFilter, setSubcategoryFilter] = useState('All');
  const [classFilter, setClassFilter] = useState('All');
  const [brandFilter, setBrandFilter] = useState('All');

  useEffect(() => {
    const fetchFilters = async () => {
      try {
        const data = await getCatalogFilters();
        setFilters(data);
      } catch (err) {
        console.error("Failed to load catalog filters", err);
      }
    };
    fetchFilters();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const params = {
        page,
        page_size: pageSize,
        sort_by: sortField,
        sort_order: sortOrder
      };
      if (search) params.search = search;
      if (categoryFilter !== 'All') params.category = categoryFilter;
      if (subcategoryFilter !== 'All') params.subcategory = subcategoryFilter;
      if (classFilter !== 'All') params.product_class = classFilter;
      if (brandFilter !== 'All') params.brand = brandFilter;

      const data = await getCatalogProducts(params);
      setProducts(data.items);
      setTotal(data.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
    // Live update for product stats
    const interval = setInterval(fetchProducts, 5000);
    return () => clearInterval(interval);
  }, [page, sortField, sortOrder, categoryFilter, subcategoryFilter, classFilter, brandFilter, search]); // Re-fetch on filter change

  const handleSort = (field) => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('desc');
    }
  };
  
  const totalPages = Math.ceil(total / pageSize) || 1;

  return (
    <div style={{ padding: '2rem', maxWidth: '1400px' }}>
      <h1 style={{ marginBottom: '0.2rem', color: 'var(--text-primary)' }}>RetailPulse Products Catalog</h1>
      <div style={{ fontSize: '1rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Dynamic Master Catalog & Live Stats</div>
      <p style={{ marginBottom: '1.5rem', fontWeight: 600, color: 'var(--success)' }}>SOURCE: DATA CATALOG / LIVE SIMULATED RETAIL DATA</p>
      
      <div className="card" style={{ marginBottom: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <input 
          type="text" 
          placeholder="Search products by ID or Name..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onBlur={() => setPage(1)} // Trigger re-fetch
          style={{ flex: 1, minWidth: '200px', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}
        />
        <select 
          value={categoryFilter} 
          onChange={(e) => { setCategoryFilter(e.target.value); setPage(1); }}
          style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
          <option value="All">All Categories</option>
          {filters.categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
        <select 
          value={subcategoryFilter} 
          onChange={(e) => { setSubcategoryFilter(e.target.value); setPage(1); }}
          style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
          <option value="All">All Subcategories</option>
          {filters.subcategories.map(sub => (
            <option key={sub} value={sub}>{sub}</option>
          ))}
        </select>
        <select 
          value={classFilter} 
          onChange={(e) => { setClassFilter(e.target.value); setPage(1); }}
          style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
          <option value="All">All Classes</option>
          {filters.product_classes.map(cls => (
            <option key={cls} value={cls}>{cls}</option>
          ))}
        </select>
        <select 
          value={brandFilter} 
          onChange={(e) => { setBrandFilter(e.target.value); setPage(1); }}
          style={{ padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
          <option value="All">All Brands</option>
          {filters.brands.map(brand => (
            <option key={brand} value={brand}>{brand}</option>
          ))}
        </select>
      </div>

      <div className="card">
        {loading && products.length === 0 ? (
          <div>Loading catalog...</div>
        ) : (
          <>
            <div style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>
              Showing {products.length} of {total} products
            </div>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid var(--border)', color: 'var(--text-muted)' }}>
                    <th style={{ padding: '0.75rem' }}>Product ID</th>
                    <th style={{ padding: '0.75rem' }}>Name</th>
                    <th style={{ padding: '0.75rem' }}>Brand</th>
                    <th style={{ padding: '0.75rem' }}>Category</th>
                    <th style={{ padding: '0.75rem' }}>Class</th>
                    <th style={{ padding: '0.75rem', cursor: 'pointer' }} onClick={() => handleSort('unit_price')}>Price {sortField === 'unit_price' ? (sortOrder === 'asc' ? '↑' : '↓') : ''}</th>
                    <th style={{ padding: '0.75rem', cursor: 'pointer', color: 'var(--primary)' }} onClick={() => handleSort('revenue')}>Live Revenue {sortField === 'revenue' ? (sortOrder === 'asc' ? '↑' : '↓') : ''}</th>
                    <th style={{ padding: '0.75rem', cursor: 'pointer', color: 'var(--primary)' }} onClick={() => handleSort('quantity')}>Live Qty {sortField === 'quantity' ? (sortOrder === 'asc' ? '↑' : '↓') : ''}</th>
                    <th style={{ padding: '0.75rem', cursor: 'pointer', color: 'var(--primary)' }} onClick={() => handleSort('transaction_count')}>Live Txns {sortField === 'transaction_count' ? (sortOrder === 'asc' ? '↑' : '↓') : ''}</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map(p => (
                    <tr key={p.product_id} style={{ borderBottom: '1px solid var(--border)' }}>
                      <td style={{ padding: '0.75rem', fontWeight: 600 }}>{p.product_id}</td>
                      <td style={{ padding: '0.75rem' }}>{p.product_name}</td>
                      <td style={{ padding: '0.75rem' }}>{p.brand}</td>
                      <td style={{ padding: '0.75rem' }}>
                        <div>{p.category}</div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{p.subcategory}</div>
                      </td>
                      <td style={{ padding: '0.75rem' }}>
                        <span style={{ 
                          padding: '0.2rem 0.5rem', 
                          borderRadius: '4px', 
                          fontSize: '0.8rem',
                          background: 'var(--bg-body)',
                          color: 'var(--text-primary)'
                        }}>
                          {p.product_class}
                        </span>
                      </td>
                      <td style={{ padding: '0.75rem' }}>₹{p.unit_price.toLocaleString()}</td>
                      <td style={{ padding: '0.75rem', color: 'var(--success)', fontWeight: 600 }}>₹{p.revenue.toLocaleString()}</td>
                      <td style={{ padding: '0.75rem' }}>{p.quantity}</td>
                      <td style={{ padding: '0.75rem' }}>{p.transaction_count}</td>
                    </tr>
                  ))}
                  {products.length === 0 && (
                    <tr>
                      <td colSpan="9" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>No products match your filters.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
              <button 
                disabled={page <= 1}
                onClick={() => setPage(page - 1)}
                style={{ padding: '0.5rem 1rem', background: 'var(--primary)', color: '#fff', border: 'none', borderRadius: '4px', cursor: page <= 1 ? 'not-allowed' : 'pointer', opacity: page <= 1 ? 0.5 : 1 }}>
                Previous
              </button>
              <span style={{ color: 'var(--text-muted)' }}>Page {page} of {totalPages}</span>
              <button 
                disabled={page >= totalPages}
                onClick={() => setPage(page + 1)}
                style={{ padding: '0.5rem 1rem', background: 'var(--primary)', color: '#fff', border: 'none', borderRadius: '4px', cursor: page >= totalPages ? 'not-allowed' : 'pointer', opacity: page >= totalPages ? 0.5 : 1 }}>
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
