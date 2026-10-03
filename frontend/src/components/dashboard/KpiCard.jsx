import React from 'react';

export default function KpiCard({ title, value, icon, loading }) {
  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1, minWidth: '200px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          {title}
        </span>
        <span style={{ fontSize: '1.2rem', opacity: 0.5 }}>{icon}</span>
      </div>
      <div style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--text-primary)' }}>
        {loading ? <span style={{ opacity: 0.5, fontSize: '1rem' }}>Loading...</span> : value}
      </div>
    </div>
  );
}
