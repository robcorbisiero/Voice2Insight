import { useState } from 'react';
import { UploadCloud, FileAudio, Loader2 } from 'lucide-react';

interface UploadSectionProps {
  onUploadComplete: (data: any) => void;
}

export default function UploadSection({ onUploadComplete }: UploadSectionProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // In local dev, Docker maps backend to 8000
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed. Must be .wav or .mp3.');
      }

      const data = await response.json();
      onUploadComplete(data);
      setFile(null); // Reset
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="glass-panel">
      <h2>New Claim Analysis</h2>
      <p className="subtitle">Upload a .wav or .mp3 audio file for AI processing.</p>
      
      <div className="upload-dropzone" onClick={() => document.getElementById('fileUpload')?.click()}>
        <input 
          id="fileUpload" 
          type="file" 
          accept=".wav,.mp3" 
          hidden 
          onChange={handleFileChange}
        />
        
        {file ? (
          <div>
            <FileAudio size={48} className="upload-icon" />
            <h3>{file.name}</h3>
            <p className="subtitle">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>
        ) : (
          <div>
            <UploadCloud size={48} className="upload-icon" />
            <h3>Drag & Drop or Click to Select</h3>
          </div>
        )}
      </div>

      {error && <p style={{ color: 'var(--accent-danger)', marginTop: '1rem' }}>{error}</p>}

      {file && (
        <button 
          className="upload-btn" 
          onClick={handleUpload} 
          disabled={isUploading}
          style={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }}
        >
          {isUploading ? <><Loader2 className="animate-spin" /> Processing AI Insights...</> : 'Analyze Claim Audio'}
        </button>
      )}
    </div>
  );
}
