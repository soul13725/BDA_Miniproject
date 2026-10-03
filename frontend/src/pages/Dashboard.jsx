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
  getCities, 
  getChannels, 
  getDailyRevenue,
  getMonthlyRevenue, 
  getTopProducts,
  getLiveSummary
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
  const [dataSource, setDataSource] = useState('LIVE'); // 'LIVE' or 'HISTORICAL'
  
  // Live chart data
  const [liveCategories, setLiveCategories] = useState([]);
  const [livePayments, setLivePayments] = useState([]);
  const [liveCities, setLiveCities] = useState([]);
  const [liveChannels, setLiveChannels] = useState([]);
  const [liveTrend, setLiveTrend] = useState([]);
  const [liveProducts, setLiveProducts] = useState([]);

  const loadHistorical = async () => {
    setLoading(true);
    try {
      const statusRes = await getAnalyticsStatus();
      setStatus(statusRes);
      if (!statusRes.analytics_available) return;

      const [sumRes, dailyRes, monthRes, catRes, payRes, cityRes, chanRes, topRes] = await Promise.all([
        getAnalyticsSummary(), getDailyRevenue(), getMonthlyRevenue(), getCategories(),
        getPayments(), getCities(), getChannels(), getTopProducts()
      ]);
      setSummary(sumRes); setDaily(dailyRes); setMonthly(monthRes); setCategories(catRes);
      setPayments(payRes); setCities(cityRes); setChannels(chanRes); setTopProducts(topRes);
    } catch (err) {
      setError(err.message);
    } finally { setLoading(false); }
  };

  const loadLive = async () => {
    try {
      const [sumRes, catRes, payRes, cityRes, chanRes, trendRes, prodRes] = await Promise.all([
        getLiveSummary(), getLiveCategories(), getLivePayments(), getLiveCities(),
        getLiveChannels(), getLiveRevenueTrend(), getLiveProducts()
      ]);
      setLiveSummary(sumRes); setLiveCategories(catRes); setLivePayments(payRes);
      setLiveCities(cityRes); setLiveChannels(chanRes); setLiveTrend(trendRes); setLiveProducts(prodRes);
    } catch (err) { console.error(err); }
  };

  useEffect(() => {
    loadHistorical();
    loadLive();
    const interval = setInterval(loadLive, 3000);
    return () => clearInterval(interval);
  }, []);

  if (error) {
    return (
      <div style={{ padding: '2rem', maxWidth: '1100px' }}>
        <div className="card" style={{ border: '1px solid var(--error)', textAlign: 'center', padding: '3rem' }}>
          <h2 style={{ color: 'var(--error)', marginBottom: '1rem' }}>Unable to connect to analytics server.</h2>
          <p style={{ color: 'var(--text-muted)' }}>Please start FastAPI.</p>
          <p style={{ fontSize: '0.8rem', marginTop: '1rem', color: 'var(--text-muted)', opacity: 0.7 }}>{error}</p>
        </div>
      </div>
    );
  }

  const isLive = dataSource === 'LIVE';

  return (
    <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '1200px' }}>
      
      {/* Header */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.2rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
            RetailPulse
            {liveSummary?.is_running ? (
               <span style={{ fontSize: '0.9rem', padding: '0.2rem 0.5rem', background: 'var(--success)', color: '#fff', borderRadius: '4px' }}>● LIVE</span>
            ) : (
               <span style={{ fontSize: '0.9rem', padding: '0.2rem 0.5rem', background: 'var(--error)', color: '#fff', borderRadius: '4px' }}>● STOPPED</span>
            )}
          </h1>
          <div style={{ fontSize: '1rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Real-Time Retail Big Data Analytics Platform</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginTop: '1rem', background: 'var(--bg-surface)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border)' }}>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Data Source</div>
              <div style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{isLive ? 'LIVE SIMULATED RETAIL DATA' : 'HISTORICAL REFERENCE DATA'}</div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Analytics Engine</div>
              <div style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{isLive ? 'LIVE ANALYTICS' : (status?.analytics_engine === 'LOCAL_FALLBACK' ? 'Local Fallback' : status?.analytics_engine)}</div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>HDFS</div>
              <div style={{ fontWeight: 500, color: status?.hdfs_available ? 'var(--success)' : 'var(--error)' }}>{status?.hdfs_available ? 'ONLINE' : 'OFFLINE'}</div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Hive</div>
              <div style={{ fontWeight: 500, color: status?.hive_available ? 'var(--success)' : 'var(--error)' }}>{status?.hive_available ? 'ONLINE' : 'OFFLINE'}</div>
            </div>
          </div>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', alignItems: 'flex-end' }}>
          <div style={{ display: 'flex', gap: '0.5rem', background: 'var(--bg-surface)', padding: '0.25rem', borderRadius: '8px', border: '1px solid var(--border)' }}>
            <button 
              onClick={() => setDataSource('LIVE')}
              style={{ padding: '0.5rem 1rem', background: isLive ? 'var(--primary)' : 'transparent', color: isLive ? '#fff' : 'var(--text-primary)', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 600 }}>
              Live Data
            </button>
            <button 
              onClick={() => setDataSource('HISTORICAL')}
              style={{ padding: '0.5rem 1rem', background: !isLive ? 'var(--primary)' : 'transparent', color: !isLive ? '#fff' : 'var(--text-primary)', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 600 }}>
              Historical Data
            </button>
          </div>
        </div>
      </header>

      {/* Infrastructure Status */}
      <section className="card" style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div style={{ width: '100%', fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem', marginBottom: '0.5rem' }}>Infrastructure Status</div>
        <div style={{ flex: 1, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem', fontSize: '0.9rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>Python</span><span style={{ color: 'var(--success)', fontWeight: 'bold' }}>ONLINE</span></div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>FastAPI</span><span style={{ color: status ? 'var(--success)' : 'var(--error)', fontWeight: 'bold' }}>{status ? 'ONLINE' : 'OFFLINE'}</span></div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>React</span><span style={{ color: 'var(--success)', fontWeight: 'bold' }}>ONLINE</span></div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>Live Analytics</span><span style={{ color: liveSummary ? 'var(--success)' : 'var(--error)', fontWeight: 'bold' }}>{liveSummary ? 'ONLINE' : 'OFFLINE'}</span></div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>Historical Dataset</span><span style={{ color: status?.dataset_exists !== false ? 'var(--success)' : 'var(--error)', fontWeight: 'bold' }}>{status?.dataset_exists !== false ? 'ONLINE' : 'OFFLINE'}</span></div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>Hadoop</span><span style={{ color: status?.hdfs_available ? 'var(--success)' : 'var(--error)', fontWeight: 'bold' }}>{status?.hdfs_available ? 'ONLINE' : 'OFFLINE'}</span></div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>HDFS</span><span style={{ color: status?.hdfs_available ? 'var(--success)' : 'var(--error)', fontWeight: 'bold' }}>{status?.hdfs_available ? 'ONLINE' : 'OFFLINE'}</span></div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}><span>Hive</span><span style={{ color: status?.hive_available ? 'var(--success)' : 'var(--error)', fontWeight: 'bold' }}>{status?.hive_available ? 'ONLINE' : 'OFFLINE'}</span></div>
        </div>
      </section>

      {isLive ? (
        <>
          {/* Live Controls */}
          <section className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Live Data Control</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontWeight: 600 }}>Status:</span>
                <span style={{ color: liveSummary?.is_running ? 'var(--success)' : 'var(--error)', fontWeight: 'bold' }}>
                  {liveSummary?.is_running ? '● RUNNING' : '○ STOPPED'}
                </span>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
              <button 
                onClick={async () => { await import('../services/api').then(m => m.startLiveStream()); loadLive(); }}
                disabled={liveSummary?.is_running}
                style={{ padding: '0.5rem 1rem', background: liveSummary?.is_running ? 'var(--muted)' : 'var(--success)', color: '#fff', border: 'none', borderRadius: '4px', cursor: liveSummary?.is_running ? 'not-allowed' : 'pointer', fontWeight: 600 }}>
                Start
              </button>
              <button 
                onClick={async () => { await import('../services/api').then(m => m.stopLiveStream()); loadLive(); }}
                disabled={!liveSummary?.is_running}
                style={{ padding: '0.5rem 1rem', background: !liveSummary?.is_running ? 'var(--muted)' : 'var(--error)', color: '#fff', border: 'none', borderRadius: '4px', cursor: !liveSummary?.is_running ? 'not-allowed' : 'pointer', fontWeight: 600 }}>
                Stop
              </button>
              <button 
                onClick={async () => { 
                  if (window.confirm("Are you sure you want to reset live data?\n\nThis will delete the current live transaction session.\nHistorical data will not be affected.")) {
                    await import('../services/api').then(m => m.resetLiveStream()); loadLive(); 
                  }
                }}
                style={{ padding: '0.5rem 1rem', background: 'transparent', color: 'var(--error)', border: '1px solid var(--error)', borderRadius: '4px', cursor: 'pointer', fontWeight: 600 }}>
                Reset
              </button>
            </div>
          </section>

          {/* Live KPIs */}
          <section style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
            <KpiCard title="Live Revenue" value={formatCurrency(liveSummary?.total_revenue)} icon="⚡" />
            <KpiCard title="Live Transactions" value={formatNumber(liveSummary?.transaction_count)} icon="⏱" />
            <KpiCard title="Live Quantity" value={formatNumber(liveSummary?.total_quantity)} icon="📦" />
            <KpiCard title="Live Avg Transaction" value={formatCurrency(liveSummary?.average_transaction_value)} icon="💳" />
            <div className="card" style={{ flex: 1, minWidth: '200px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Live Session</div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Latest Transaction</div>
              <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{liveSummary?.latest_timestamp ? new Date(liveSummary.latest_timestamp).toLocaleTimeString() : 'Waiting...'}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                Last updated: {new Date().toLocaleTimeString()}
              </div>
            </div>
          </section>

          {/* Live Charts */}
          <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '1.5rem' }}>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Live Revenue Trend (Recent)</h3>
              <RevenueTrendChart data={liveTrend} />
            </div>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Live Category Revenue</h3>
              <CategoryChart data={liveCategories} />
            </div>
          </section>

          <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '1.5rem' }}>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Live Payment Methods</h3>
              <PaymentChart data={livePayments} />
            </div>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Live City Analysis</h3>
              <CityChart data={liveCities} />
            </div>
          </section>

          <section>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Live Top Products</h3>
              <AnalyticsTable data={liveProducts} />
            </div>
          </section>
        </>
      ) : (
        <>
          {/* Historical KPIs */}
          <section style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
            <KpiCard title="Historical Revenue" value={formatCurrency(summary?.total_revenue)} icon="₹" loading={loading} />
            <KpiCard title="Historical Transactions" value={formatNumber(summary?.total_transactions)} icon="📈" loading={loading} />
            <KpiCard title="Historical Quantity" value={formatNumber(summary?.total_quantity)} icon="📦" loading={loading} />
            <KpiCard title="Avg Transaction" value={formatCurrency(summary?.average_transaction_value)} icon="💳" loading={loading} />
          </section>

          {/* Historical Charts */}
          <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '1.5rem' }}>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Revenue Trend</h3>
              {loading ? <div>Loading...</div> : <RevenueTrendChart data={daily} />}
            </div>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Monthly Revenue</h3>
              {loading ? <div>Loading...</div> : <MonthlyRevenueChart data={monthly} />}
            </div>
          </section>

          <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '1.5rem' }}>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Category Revenue</h3>
              {loading ? <div>Loading...</div> : <CategoryChart data={categories} />}
            </div>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Payment Methods</h3>
              {loading ? <div>Loading...</div> : <PaymentChart data={payments} />}
            </div>
          </section>

          <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '1.5rem' }}>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>City Analysis</h3>
              {loading ? <div>Loading...</div> : <CityChart data={cities} />}
            </div>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Sales Channel</h3>
              {loading ? <div>Loading...</div> : <ChannelChart data={channels} />}
            </div>
          </section>

          <section>
            <div className="card">
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--text-primary)' }}>Top Products</h3>
              {loading ? <div>Loading...</div> : <AnalyticsTable data={topProducts} />}
            </div>
          </section>
        </>
      )}
    </div>
  );
}
