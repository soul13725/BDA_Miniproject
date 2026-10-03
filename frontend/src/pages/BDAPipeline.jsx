import React, { useState, useEffect } from 'react';
import { getAnalyticsStatus, getLiveStatus, getInfrastructureStatus } from '../services/api';

export default function BDAPipeline() {
  const [analyticsStatus, setAnalyticsStatus] = useState(null);
  const [liveStatus, setLiveStatus] = useState(null);
  const [infraStatus, setInfraStatus] = useState(null);

  useEffect(() => {
    getAnalyticsStatus().then(setAnalyticsStatus).catch(console.error);
    getLiveStatus().then(setLiveStatus).catch(console.error);
    getInfrastructureStatus().then(setInfraStatus).catch(console.error);
  }, []);

  const liveComponents = [
    { name: "CANONICAL CATALOG\ndata/catalog/", status: "ONLINE", active: true },
    { name: "LIVE GENERATOR\nretail_live_transactions", status: liveStatus?.is_running ? 'ONLINE' : 'OFFLINE', active: !!liveStatus?.is_running },
    { name: "LIVE CSV\ndata/live/retail_live_transactions.csv", status: "ONLINE", active: true },
    { name: "LIVE ANALYTICS\nIn-Memory Aggregation", status: "ONLINE", active: true },
    { name: "FASTAPI\nBackend Analytics API", status: infraStatus?.fastapi === 'ONLINE' ? 'ONLINE' : 'OFFLINE', active: infraStatus?.fastapi === 'ONLINE' },
    { name: "REACT DASHBOARD\nRetailPulse UI", status: infraStatus?.react === 'ONLINE' ? 'ONLINE' : 'OFFLINE', active: infraStatus?.react === 'ONLINE' }
  ];

  const histComponents = [
    { name: "HISTORICAL CSV\ndata/retail_logs.csv", status: infraStatus?.historical_dataset === 'ONLINE' ? 'ONLINE' : 'OFFLINE', active: infraStatus?.historical_dataset === 'ONLINE' },
    { name: "HDFS\n/retail_bda/raw", status: infraStatus?.hdfs === 'ONLINE' ? 'ONLINE' : 'OFFLINE', active: infraStatus?.hdfs === 'ONLINE' },
    { name: "MapReduce\nPython Mapper/Reducer", status: infraStatus?.mapreduce === 'ONLINE' ? 'REAL HADOOP' : 'LOCAL SIMULATION', active: true },
    { name: "MapReduce Output\noutput/mapreduce", status: infraStatus?.mapreduce_output === 'ONLINE' ? 'ONLINE' : (infraStatus?.mapreduce_output || "LOCAL OUTPUT"), active: true },
    { name: "Hive\nApache Hive Data Warehouse", status: infraStatus?.hive === 'ONLINE' ? 'ONLINE' : 'OFFLINE', active: infraStatus?.hive === 'ONLINE' },
    { name: "HiveQL / Analytics\noutput/hive", status: infraStatus?.hiveql === 'ONLINE' ? 'ONLINE' : 'LOCAL FALLBACK', active: true },
    { name: "FASTAPI\nBackend Analytics API", status: infraStatus?.fastapi === 'ONLINE' ? 'ONLINE' : 'OFFLINE', active: infraStatus?.fastapi === 'ONLINE' },
    { name: "REACT DASHBOARD\nRetailPulse UI", status: infraStatus?.react === 'ONLINE' ? 'ONLINE' : 'OFFLINE', active: infraStatus?.react === 'ONLINE' }
  ];

  const PipelineFlow = ({ components, fallbackMessage }) => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', flex: 1, minWidth: '300px' }}>
      {components.map((comp, idx) => (
        <div key={comp.name + idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <div className="card" style={{ 
            width: '100%',
            maxWidth: '400px',
            border: `2px solid ${comp.active ? 'var(--primary)' : 'var(--border)'}`,
            opacity: comp.active ? 1 : 0.7,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            textAlign: 'center'
          }}>
            <h3 style={{ margin: 0, whiteSpace: 'pre-wrap', textAlign: 'left', fontSize: '1rem' }}>{comp.name}</h3>
            <span style={{ 
              fontWeight: 'bold', 
              color: comp.status.includes('ONLINE') ? 'var(--success)' : 'var(--error)' 
            }}>
              {comp.status.includes('ONLINE') ? '✓ ' : '✗ '}{comp.status}
            </span>
          </div>
          {idx < components.length - 1 && (
            <div style={{ 
              height: '30px', 
              width: '4px', 
              background: 'var(--primary)', 
              opacity: 0.3
            }} />
          )}
        </div>
      ))}
      {fallbackMessage && (
        <div style={{ textAlign: 'center', marginTop: '1rem', color: 'var(--text-muted)', fontSize: '0.9rem', fontStyle: 'italic' }}>
          {fallbackMessage}
        </div>
      )}
    </div>
  );

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px' }}>
      <h1 style={{ marginBottom: '0.2rem', color: 'var(--text-primary)' }}>RetailPulse BDA Pipeline</h1>
      <div style={{ fontSize: '1rem', color: 'var(--text-muted)', marginBottom: '2rem' }}>Real-Time Big Data Processing Flow</div>
      
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4rem' }}>
        <div style={{ flex: 1, minWidth: '350px' }}>
          <h2 style={{ marginBottom: '1.5rem', color: 'var(--text-primary)', borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>Live Stream Architecture</h2>
          <PipelineFlow components={liveComponents} />
        </div>
        
        <div style={{ flex: 1, minWidth: '350px' }}>
          <h2 style={{ marginBottom: '1.5rem', color: 'var(--text-primary)', borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>Historical BDA Processing</h2>
          <PipelineFlow 
            components={histComponents} 
            fallbackMessage={!analyticsStatus?.hive_available ? "Local analytics fallback is active. HDFS/Hive infrastructure is currently unavailable." : ""}
          />
        </div>
      </div>
    </div>
  );
}
