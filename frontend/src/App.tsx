import { useState } from 'react';
import UploadSection from './components/UploadSection';
import Dashboard from './components/Dashboard';

function App() {
  const [claims, setClaims] = useState<any[]>([]);

  const handleUploadComplete = (data: any) => {
    // Add the new claim to the top of the list
    setClaims(prev => [data, ...prev]);
  };

  return (
    <div className="app-container">
      <header>
        <h1>Voice2Insight</h1>
        <p className="subtitle">AI-Powered Claims Assistant & PII Redaction</p>
      </header>
      
      <main>
        <UploadSection onUploadComplete={handleUploadComplete} />
        <Dashboard claims={claims} />
      </main>
    </div>
  );
}

export default App;
