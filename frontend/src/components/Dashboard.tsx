import { useState } from 'react';
import ClaimCard from './ClaimCard';

interface DashboardProps {
  claims: any[];
}

export default function Dashboard({ claims }: DashboardProps) {
  
  if (claims.length === 0) {
    return (
      <div style={{ textAlign: 'center', marginTop: '3rem', color: 'var(--text-muted)' }}>
        No claims processed yet. Upload an audio file to begin.
      </div>
    );
  }

  return (
    <div className="dashboard-grid">
      {claims.map((claim) => (
        <ClaimCard key={claim.id} claim={claim} />
      ))}
    </div>
  );
}
