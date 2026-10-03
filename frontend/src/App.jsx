import { NavLink, Routes, Route } from 'react-router-dom';

import Dashboard from './pages/Dashboard.jsx';
import Products from './pages/Products.jsx';
import Transactions from './pages/Transactions.jsx';


/* ============================================================
   App — Phase 01 Shell
   ============================================================ */

// ── Nav item definition ──────────────────────────────────────
const NAV_ITEMS = [
  { path: '/',             label: 'Dashboard',    icon: '⬡' },
  { path: '/products',     label: 'Products',     icon: '🛒' },
  { path: '/transactions', label: 'Transactions', icon: '💳' },
];

// ── Tech stack badges ────────────────────────────────────────
const TECH_STACK = [
  { label: 'React + Vite',  variant: 'primary',   status: 'active',  note: 'Frontend'          },
  { label: 'FastAPI',       variant: 'primary',   status: 'active',  note: 'Backend API'        },
];

/* ── Sidebar ── */
function Sidebar() {
  return (
    <aside style={styles.sidebar}>
      {/* Logo */}
      <div style={styles.logo}>
        <span style={styles.logoIcon}>📊</span>
        <div>
          <div style={styles.logoTitle}>RetailPulse</div>
          <div style={styles.logoSub}>Real-Time Retail Analytics</div>
        </div>
      </div>

      {/* Nav */}
      <nav style={styles.nav}>
        <div style={styles.navLabel}>Navigation</div>
        {NAV_ITEMS.map(({ path, label, icon }) => (
          <NavLink
            key={path}
            to={path}
            end={path === '/'}
            style={({ isActive }) => ({
              ...styles.navItem,
              ...(isActive ? styles.navItemActive : {}),
            })}
          >
            <span style={styles.navIcon}>{icon}</span>
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div style={styles.sidebarFooter}>
        <span className="badge badge--muted">v0.1.0</span>
      </div>
    </aside>
  );
}

/* ── App Shell ── */


/* ── Placeholder Page ── */
function PlaceholderPage({ title }) {
  return (
    <div style={styles.page}>
      <div className="card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🚧</div>
        <h2 style={{ color: 'var(--text-primary)', marginBottom: '0.75rem' }}>{title}</h2>
        <p style={{ marginBottom: '1.5rem' }}>
          This section will be implemented in a future phase.
        </p>
        <span className="badge badge--secondary">Coming Soon</span>
      </div>
    </div>
  );
}

/* ── Root App ── */
export default function App() {
  return (
    <div style={styles.layout}>
      <Sidebar />
      <main style={styles.main}>
        <Routes>
          <Route path="/"             element={<Dashboard />} />
          <Route path="/products"     element={<Products />} />
          <Route path="/transactions" element={<Transactions />} />
        </Routes>
      </main>
    </div>
  );
}

/* ============================================================
   Inline styles — keeps the component self-contained
   and works without any CSS framework.
   ============================================================ */
const styles = {
  layout: {
    display: 'flex',
    minHeight: '100vh',
    backgroundColor: 'var(--bg-base)',
  },
  sidebar: {
    width: '240px',
    flexShrink: 0,
    backgroundColor: 'var(--bg-surface)',
    borderRight: '1px solid var(--border)',
    display: 'flex',
    flexDirection: 'column',
    padding: '1.5rem 1rem',
    position: 'sticky',
    top: 0,
    height: '100vh',
    overflowY: 'auto',
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    marginBottom: '2rem',
    padding: '0 0.5rem',
  },
  logoIcon: { fontSize: '1.75rem' },
  logoTitle: {
    fontSize: '1rem',
    fontWeight: 700,
    color: 'var(--text-primary)',
    lineHeight: 1.2,
  },
  logoSub: {
    fontSize: '0.7rem',
    color: 'var(--text-muted)',
    letterSpacing: '0.04em',
  },
  nav: { display: 'flex', flexDirection: 'column', gap: '0.25rem', flex: 1 },
  navLabel: {
    fontSize: '0.65rem',
    fontWeight: 600,
    color: 'var(--text-muted)',
    letterSpacing: '0.1em',
    textTransform: 'uppercase',
    padding: '0 0.5rem',
    marginBottom: '0.5rem',
  },
  navItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.6rem',
    padding: '0.65rem 0.75rem',
    borderRadius: 'var(--radius-sm)',
    fontSize: '0.875rem',
    fontWeight: 500,
    color: 'var(--text-secondary)',
    textDecoration: 'none',
    transition: 'background var(--transition), color var(--transition)',
    position: 'relative',
  },
  navItemActive: {
    backgroundColor: 'var(--primary-glow)',
    color: 'var(--primary)',
  },
  navIcon: { fontSize: '1rem', width: '1.25rem', textAlign: 'center' },
  navBadge: {
    marginLeft: 'auto',
    fontSize: '0.6rem',
    fontWeight: 600,
    color: 'var(--text-muted)',
    backgroundColor: 'var(--bg-elevated)',
    padding: '0.15rem 0.4rem',
    borderRadius: '999px',
    border: '1px solid var(--border)',
  },
  sidebarFooter: {
    paddingTop: '1rem',
    borderTop: '1px solid var(--border)',
    display: 'flex',
    justifyContent: 'center',
  },
  main: {
    flex: 1,
    overflowY: 'auto',
    backgroundColor: 'var(--bg-base)',
  },
  page: {
    padding: '2rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '2.5rem',
    maxWidth: '1100px',
  },

  /* Hero */
  hero: {
    position: 'relative',
    padding: '2.5rem',
    backgroundColor: 'var(--bg-surface)',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius-lg)',
    overflow: 'hidden',
  },
  heroAccent: {
    position: 'absolute',
    top: 0, right: 0,
    width: '350px', height: '350px',
    background: 'radial-gradient(circle, var(--primary-glow) 0%, transparent 70%)',
    pointerEvents: 'none',
  },
  heroBadgeRow: {
    display: 'flex',
    gap: '0.75rem',
    flexWrap: 'wrap',
    marginBottom: '1.25rem',
  },
  heroTitle: {
    fontSize: 'clamp(2rem, 4vw, 3.25rem)',
    fontWeight: 800,
    color: 'var(--text-primary)',
    marginBottom: '0.5rem',
    lineHeight: 1.1,
  },
  heroAccentText: {
    background: 'linear-gradient(135deg, var(--primary), var(--secondary))',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
  },
  heroSubtitle: {
    fontSize: '1.125rem',
    fontWeight: 500,
    color: 'var(--text-secondary)',
    marginBottom: '1rem',
  },
  heroDesc: {
    fontSize: '0.9rem',
    color: 'var(--text-muted)',
    maxWidth: '620px',
    lineHeight: 1.7,
  },

  /* Status Row */
  statusRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
    gap: '1rem',
  },
  statusCard: { display: 'flex', flexDirection: 'column' },
  statusCardLabel: {
    fontSize: '0.75rem',
    fontWeight: 600,
    color: 'var(--text-muted)',
    textTransform: 'uppercase',
    letterSpacing: '0.08em',
  },

  /* Section */
  sectionTitle: {
    fontSize: '1.125rem',
    fontWeight: 700,
    color: 'var(--text-primary)',
    marginBottom: '1rem',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },

  /* Tech Grid */
  techGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: '1rem',
  },
  techCard: { display: 'flex', flexDirection: 'column', gap: '0.75rem' },
  techCardTop: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' },
  techCardNote: { fontSize: '0.8rem', color: 'var(--text-muted)' },

  /* Roadmap */
  roadmapGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: '1rem',
  },
  roadmapCard: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  roadmapCardCurrent: {
    borderColor: 'var(--primary)',
    boxShadow: '0 0 16px var(--primary-glow)',
  },
  roadmapPhase: {
    fontSize: '0.7rem',
    fontWeight: 700,
    color: 'var(--text-muted)',
    textTransform: 'uppercase',
    letterSpacing: '0.1em',
  },
  roadmapTitle: {
    fontSize: '0.875rem',
    fontWeight: 600,
    color: 'var(--text-primary)',
    lineHeight: 1.3,
    flex: 1,
  },
};
