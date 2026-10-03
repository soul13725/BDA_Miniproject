import React from 'react';
import { 
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, 
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend 
} from 'recharts';

const COLORS = ['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#ec4899'];

export function RevenueTrendChart({ data }) {
  if (!data || data.length === 0) return <div>No analytics data available.</div>;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 10, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
        <XAxis dataKey="date" stroke="#888" tick={{fontSize: 12}} />
        <YAxis stroke="#888" tick={{fontSize: 12}} />
        <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', border: '1px solid #333' }} />
        <Line type="monotone" dataKey="revenue" stroke="#8b5cf6" strokeWidth={3} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function MonthlyRevenueChart({ data }) {
  if (!data || data.length === 0) return <div>No analytics data available.</div>;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} margin={{ top: 10, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
        <XAxis dataKey="month" stroke="#888" tick={{fontSize: 12}} />
        <YAxis stroke="#888" tick={{fontSize: 12}} />
        <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', border: '1px solid #333' }} />
        <Bar dataKey="revenue" fill="#3b82f6" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function CategoryChart({ data }) {
  if (!data || data.length === 0) return <div>No analytics data available.</div>;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie data={data} dataKey="revenue" nameKey="category" cx="50%" cy="50%" innerRadius={60} outerRadius={100} fill="#8884d8" paddingAngle={5} label>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', border: '1px solid #333' }} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function PaymentChart({ data }) {
  if (!data || data.length === 0) return <div>No analytics data available.</div>;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
        <XAxis type="number" stroke="#888" />
        <YAxis dataKey="payment_method" type="category" stroke="#888" width={80} />
        <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', border: '1px solid #333' }} />
        <Bar dataKey="revenue" fill="#10b981" radius={[0, 4, 4, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function CityChart({ data }) {
  if (!data || data.length === 0) return <div>No analytics data available.</div>;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} margin={{ top: 10, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
        <XAxis dataKey="city" stroke="#888" tick={{fontSize: 12}} />
        <YAxis stroke="#888" tick={{fontSize: 12}} />
        <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', border: '1px solid #333' }} />
        <Bar dataKey="revenue" fill="#f59e0b" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function ChannelChart({ data }) {
  if (!data || data.length === 0) return <div>No analytics data available.</div>;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie data={data} dataKey="revenue" nameKey="channel" cx="50%" cy="50%" innerRadius={40} outerRadius={100} fill="#8884d8" paddingAngle={5} label>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[(index + 4) % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', border: '1px solid #333' }} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function AnalyticsTable({ data }) {
  if (!data || data.length === 0) return <div>No analytics data available.</div>;
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid var(--border)', color: 'var(--text-muted)' }}>
            <th style={{ padding: '0.75rem 0.5rem' }}>Rank</th>
            <th style={{ padding: '0.75rem 0.5rem' }}>Product ID</th>
            <th style={{ padding: '0.75rem 0.5rem' }}>Product Name</th>
            <th style={{ padding: '0.75rem 0.5rem', textAlign: 'right' }}>Revenue</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, idx) => (
            <tr key={item.product_id} style={{ borderBottom: '1px solid var(--border)' }}>
              <td style={{ padding: '0.75rem 0.5rem' }}>{idx + 1}</td>
              <td style={{ padding: '0.75rem 0.5rem', color: 'var(--text-muted)' }}>{item.product_id}</td>
              <td style={{ padding: '0.75rem 0.5rem', fontWeight: 500 }}>{item.product_name}</td>
              <td style={{ padding: '0.75rem 0.5rem', textAlign: 'right' }}>
                {new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(item.revenue)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
