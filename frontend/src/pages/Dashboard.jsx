import React, { useState, useEffect } from 'react';
import KpiCard from '../components/dashboard/KpiCard';
import { 
  RevenueTrendChart, 
  MonthlyRevenueChart, 
  CategoryChart, 
  PaymentChart, 
  CityChart, 
  ChannelChart, 
  AnalyticsTable 
} from '../components/dashboard/Charts';
import { 
  getAnalyticsStatus, 
  getAnalyticsSummary, 
  getCategories, 
  getPayments, 
  getCities, 
  getChannels, 
  getDailyRevenue, 
  getMonthlyRevenue, 
  getTopProducts 
} from '../services/api';

const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(val || 0);
const formatNumber = (val) => new Intl.NumberFormat('en-IN').format(val || 0);

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [status, setStatus] = useState(null);
  const [summary, setSummary] = useState(null);
  const [daily, setDaily] = useState([]);
  const [monthly, setMonthly] = useState([]);
  const [categories, setCategories] = useState([]);
  const [payments, setPayments] = useState([]);
  const [cities, setCities] = useState([]);
  const [channels, setChannels] = useState([]);
  const [topProducts, setTopProducts] = useState([]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const statusRes = await getAnalyticsStatus();
      setStatus(statusRes);

      if (!statusRes.analytics_available) {
        throw new Error("Phase 05 analytics must be generated before viewing dashboard.");
      }

      const [
        sumRes, dailyRes, monthRes, catRes, payRes, cityRes, chanRes, topRes
      ] = await Promise.all([
        getAnalyticsSummary(),
        getDailyRevenue(),
        getMonthlyRevenue(),
        getCategories(),
        getPayments(),
        getCities(),
        getChannels(),
        getTopProducts()
      ]);

      setSummary(sumRes);
      setDaily(dailyRes);
      setMonthly(monthRes);
      setCategories(catRes);
      setPayments(payRes);
      setCities(cityRes);
      setChannels(chanRes);
      setTopProducts(topRes);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || "Unable to load analytics data. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (error) {
    return (
      <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '1100px' }}>
        <div className="card" style={{ border: '1px solid var(--error)' }}>
          <h2 style={{ color: 'var(--error)', marginBottom: '1rem' }}>Error Loading Dashboard</h2>
          <p>{error}</p>
          <button 
            onClick={loadData}
            style={{ marginTop: '1rem', padding: '0.5rem 1rem', background: 'var(--primary)', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '1200px' }}>
      
      {/* Header */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
            Retail BDA Analytics
          </h1>
          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            <span className="badge badge--primary">
              Analytics Engine: {status ? status.analytics_engine : 'Loading...'}
            </span>
            <span className="badge badge--muted">
              HDFS: {status?.hdfs_available ? 'Available' : 'Unavailable'}
            </span>
            <span className="badge badge--muted">
              Hive: {status?.hive_available ? 'Available' : 'Unavailable'}
            </span>
          </div>
        </div>
        <button 
          onClick={loadData}
          disabled={loading}
          style={{ padding: '0.5rem 1rem', background: 'var(--bg-surface)', color: 'var(--text-primary)', border: '1px solid var(--border)', borderRadius: '4px', cursor: loading ? 'not-allowed' : 'pointer' }}>
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </header>

      {/* KPIs */}
      <section style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
        <KpiCard title="Total Revenue" value={formatCurrency(summary?.total_revenue)} icon="₹" loading={loading} />
        <KpiCard title="Transactions" value={formatNumber(summary?.total_transactions)} icon="📈" loading={loading} />
        <KpiCard title="Total Quantity" value={formatNumber(summary?.total_quantity)} icon="📦" loading={loading} />
        <KpiCard title="Avg Transaction" value={formatCurrency(summary?.average_transaction_value)} icon="💳" loading={loading} />
      </section>

      {/* Charts Grid */}
      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '1.5rem' }}>
        <div className="card">
          <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Revenue Trend</h3>
          {loading ? <div>Loading analytics...</div> : <RevenueTrendChart data={daily} />}
        </div>
        <div className="card">
          <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Monthly Revenue</h3>
          {loading ? <div>Loading analytics...</div> : <MonthlyRevenueChart data={monthly} />}
        </div>
      </section>

      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '1.5rem' }}>
        <div className="card">
          <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Category Revenue</h3>
          {loading ? <div>Loading analytics...</div> : <CategoryChart data={categories} />}
        </div>
        <div className="card">
          <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Payment Methods</h3>
          {loading ? <div>Loading analytics...</div> : <PaymentChart data={payments} />}
        </div>
      </section>

      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '1.5rem' }}>
        <div className="card">
          <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>City Analysis</h3>
          {loading ? <div>Loading analytics...</div> : <CityChart data={cities} />}
        </div>
        <div className="card">
          <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Sales Channel</h3>
          {loading ? <div>Loading analytics...</div> : <ChannelChart data={channels} />}
        </div>
      </section>

      <section>
        <div className="card">
          <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Top Products</h3>
          {loading ? <div>Loading analytics...</div> : <AnalyticsTable data={topProducts} />}
        </div>
      </section>

    </div>
  );
}
