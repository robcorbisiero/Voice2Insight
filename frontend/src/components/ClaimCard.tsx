import { Activity, User, MapPin, Clock, ShieldCheck } from 'lucide-react';

interface Insight {
  sentiment: string;
  urgency_score: number;
  claimant_name: string | null;
  location: string | null;
  incident_time: string | null;
}

interface ClaimProps {
  claim: {
    id: string;
    transcript: string;
    insights: Insight;
  };
}

export default function ClaimCard({ claim }: ClaimProps) {
  const { insights } = claim;

  const getSentimentBadge = (sentiment: string) => {
    const s = sentiment.toLowerCase();
    let badgeClass = 'badge-calm';
    if (s.includes('frustrated')) badgeClass = 'badge-frustrated';
    if (s.includes('distressed')) badgeClass = 'badge-distressed';
    return <span className={badgeClass}>{sentiment}</span>;
  };

  return (
    <div className="glass-panel claim-card">
      <div className="claim-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <ShieldCheck size={24} color="var(--accent-primary)" />
          <h3>Claim Analysis</h3>
        </div>
        <span className="claim-id">ID: {claim.id.substring(0,8)}...</span>
      </div>

      <div className="claim-content">
        <div className="transcript-panel">
          <p className="subtitle" style={{marginBottom: '1rem'}}>Redacted Transcript</p>
          <div className="transcript-text">
            {claim.transcript}
          </div>
        </div>

        <div className="insights-panel">
          <p className="subtitle">AI Insights (Gemini 1.5 Pro)</p>
          
          <div className="insight-item">
            <span className="insight-label"><Activity size={16}/> Sentiment</span>
            <span className="insight-value">{getSentimentBadge(insights.sentiment)}</span>
          </div>
          
          <div className="insight-item">
            <span className="insight-label"><Activity size={16}/> Urgency Score</span>
            <span className="insight-value" style={{color: insights.urgency_score >= 7 ? 'var(--accent-danger)' : 'inherit'}}>
              {insights.urgency_score} / 10
            </span>
          </div>

          <div className="insight-item">
            <span className="insight-label"><User size={16}/> Claimant</span>
            <span className="insight-value">{insights.claimant_name || 'N/A'}</span>
          </div>

          <div className="insight-item">
            <span className="insight-label"><MapPin size={16}/> Location</span>
            <span className="insight-value">{insights.location || 'N/A'}</span>
          </div>

          <div className="insight-item">
            <span className="insight-label"><Clock size={16}/> Time</span>
            <span className="insight-value">{insights.incident_time || 'N/A'}</span>
          </div>
        </div>
      </div>
      
      {/* 
        Below we would wire up the Redacted Audio URL if we were returning the file blob or URL from Supabase 
        For demonstration, we mock the player.
      */}
      <div className="audio-player">
        <p className="subtitle" style={{marginBottom: '0.5rem', fontSize: '0.9rem'}}>Redacted Audio Player (PII Muted)</p>
        <audio controls src="https://www.learningcontainer.com/wp-content/uploads/2020/02/Kalimba.mp3"></audio>
      </div>
    </div>
  );
}
