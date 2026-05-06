import React, { useState, useCallback, useRef } from 'react';
import { Upload, Camera, Shield, Cpu, Activity, Info, CheckCircle, Loader2, AlertCircle } from 'lucide-react';

const API_BASE = "http://localhost:8000";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleUpload = async (file) => {
    if (!file) return;
    
    setLoading(true);
    setError(null);
    setResults(null);
    
    // Preview
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(file);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Analysis failed');

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const onFileChange = (e) => {
    handleUpload(e.target.files[0]);
  };

  const triggerUpload = () => fileInputRef.current.click();

  return (
    <div className="dashboard">
      {/* Background Effect */}
      <div className="bg-grid"></div>
      
      {/* Sidebar / Header */}
      <header className="glass">
        <div className="logo">
          <Shield className="icon-accent" />
          <h1 style={{ fontFamily: 'Orbitron' }}>DRONE VISION <span className="subtext">PRO</span></h1>
        </div>
        <div className="status-pills">
          <div className="pill"><Activity size={14} /> SYSTEM: ONLINE</div>
          <div className="pill"><Cpu size={14} /> AI: YOLOv8 + CLIP</div>
        </div>
      </header>

      <main>
        {/* Left Panel: Image View */}
        <section className="viewport-container">
          <div className="glass viewport">
            {!preview ? (
              <div className="upload-placeholder" onClick={triggerUpload}>
                <Upload size={48} className="icon-accent mb-4" />
                <h3>Initialize Scan</h3>
                <p>Drag and drop or click to upload drone footage</p>
                <input 
                  type="file" 
                  hidden 
                  ref={fileInputRef} 
                  onChange={onFileChange}
                  accept="image/*"
                />
              </div>
            ) : (
              <div className="image-display">
                <img 
                  src={results ? `${API_BASE}${results.annotated_url}` : preview} 
                  alt="Drone View" 
                  className={loading ? 'scanning' : ''}
                />
                {loading && <div className="scan-line"></div>}
              </div>
            )}
          </div>
          
          {error && (
            <div className="error-card glass">
              <AlertCircle className="icon-error" />
              <span>{error}</span>
            </div>
          )}
        </section>

        {/* Right Panel: Data Analysis */}
        <section className="data-panel">
          <div className="glass panel-header">
            <Info size={18} className="icon-accent" />
            <h2>Telemetry & Analysis</h2>
          </div>

          <div className="results-container">
            {loading ? (
              <div className="loading-state">
                <Loader2 className="spinner" size={32} />
                <p>Neural Processing in progress...</p>
              </div>
            ) : results ? (
              <div className="results-list">
                <div className="stats-grid mb-6">
                  <div className="stat-item glass highlight">
                    <span className="label">Global Theme</span>
                    <span className="value theme-text">{results.scene.theme}</span>
                  </div>
                  <div className="stat-item glass">
                    <span className="label">Detections</span>
                    <span className="value">{results.objects.length}</span>
                  </div>
                </div>

                <div className="stats-grid mb-6">
                  <div className="stat-item glass">
                    <span className="label">Scene Confidence</span>
                    <span className="value">{(results.scene.theme_confidence * 100).toFixed(0)}%</span>
                  </div>
                  <div className="stat-item glass">
                    <span className="label">Max Object Conf.</span>
                    <span className="value">{(Math.max(...results.objects.map(o => o.confidence), 0) * 100).toFixed(0)}%</span>
                  </div>
                </div>

                {results.objects.map((obj, i) => (
                  <div key={i} className="object-card glass fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
                    <div className="card-image">
                      <img src={`${API_BASE}${obj.crop_url}`} alt={obj.label} />
                    </div>
                    <div className="card-info">
                      <div className="card-header">
                        <span className="tag">{obj.label.toUpperCase()}</span>
                        <span className="confidence">{(obj.confidence * 100).toFixed(0)}%</span>
                      </div>
                      <h3>{obj.specific_detail}</h3>
                      <div className="detail-meta">
                        <CheckCircle size={12} className="icon-success" />
                        <span>Analysis Confidence: {(obj.detail_confidence * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <Camera size={32} className="icon-dim mb-2" />
                <p>Awaiting data feed...</p>
              </div>
            )}
          </div>
        </section>
      </main>

      <style jsx>{`
        .dashboard {
          display: flex;
          flex-direction: column;
          height: 100%;
          padding: 20px;
          gap: 20px;
          position: relative;
          z-index: 1;
        }

        .bg-grid {
          position: fixed;
          top: 0; left: 0; right: 0; bottom: 0;
          background-image: radial-gradient(circle at 2px 2px, rgba(0, 242, 255, 0.05) 1px, transparent 0);
          background-size: 40px 40px;
          z-index: -1;
        }

        header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 15px 25px;
          flex-shrink: 0;
        }

        .logo {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .logo h1 {
          font-size: 20px;
          letter-spacing: 2px;
        }

        .subtext {
          font-size: 12px;
          color: var(--accent-color);
          font-family: 'Inter';
        }

        .status-pills {
          display: flex;
          gap: 15px;
        }

        .pill {
          font-size: 11px;
          font-weight: 600;
          padding: 5px 12px;
          border-radius: 20px;
          background: rgba(0, 242, 255, 0.1);
          color: var(--accent-color);
          display: flex;
          align-items: center;
          gap: 6px;
          border: 1px solid rgba(0, 242, 255, 0.2);
        }

        main {
          display: grid;
          grid-template-columns: 1.5fr 1fr;
          gap: 20px;
          flex-grow: 1;
          overflow: hidden;
        }

        .viewport-container {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }

        .viewport {
          flex-grow: 1;
          display: flex;
          justify-content: center;
          align-items: center;
          position: relative;
          overflow: hidden;
          background: #000;
        }

        .upload-placeholder {
          text-align: center;
          cursor: pointer;
          transition: all 0.3s ease;
          padding: 40px;
          border: 2px dashed var(--border-color);
          border-radius: 20px;
        }

        .upload-placeholder:hover {
          border-color: var(--accent-color);
          background: rgba(0, 242, 255, 0.05);
        }

        .image-display {
          width: 100%;
          height: 100%;
          display: flex;
          justify-content: center;
          align-items: center;
          position: relative;
        }

        .image-display img {
          max-width: 100%;
          max-height: 100%;
          object-fit: contain;
        }

        .scanning {
          filter: grayscale(0.5) brightness(0.8);
        }

        .scan-line {
          position: absolute;
          top: 0; left: 0; right: 0;
          height: 2px;
          background: var(--accent-color);
          box-shadow: 0 0 15px var(--accent-color);
          animation: scan 2s linear infinite;
        }

        .data-panel {
          display: flex;
          flex-direction: column;
          gap: 15px;
          overflow: hidden;
        }

        .panel-header {
          padding: 15px 20px;
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .panel-header h2 {
          font-size: 16px;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .results-container {
          flex-grow: 1;
          overflow-y: auto;
          padding-right: 5px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 12px;
        }

        .stat-item {
          padding: 12px;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 4px;
        }

        .stat-item .label {
          font-size: 10px;
          color: var(--text-secondary);
          text-transform: uppercase;
        }

        .stat-item .value {
          font-size: 24px;
          font-weight: 700;
          color: var(--accent-color);
          font-family: 'Orbitron';
        }

        .theme-text {
          font-size: 16px !important;
          text-transform: uppercase;
        }

        .highlight {
          border: 1px solid var(--accent-color) !important;
          background: rgba(0, 242, 255, 0.05) !important;
          grid-column: span 2;
        }

        .object-card {
          display: flex;
          gap: 15px;
          padding: 12px;
          margin-bottom: 12px;
          transition: transform 0.2s ease;
        }

        .object-card:hover {
          transform: translateX(5px);
          border-color: var(--accent-color);
        }

        .card-image {
          width: 80px;
          height: 80px;
          border-radius: 8px;
          overflow: hidden;
          flex-shrink: 0;
          border: 1px solid var(--border-color);
        }

        .card-image img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .card-info {
          flex-grow: 1;
          display: flex;
          flex-direction: column;
          justify-content: center;
          gap: 4px;
        }

        .card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .tag {
          font-size: 10px;
          font-weight: 700;
          padding: 2px 8px;
          background: var(--accent-color);
          color: #000;
          border-radius: 4px;
        }

        .confidence {
          font-size: 11px;
          color: var(--text-secondary);
        }

        .card-info h3 {
          font-size: 14px;
          font-weight: 600;
          color: var(--text-primary);
        }

        .detail-meta {
          display: flex;
          align-items: center;
          gap: 5px;
          font-size: 11px;
          color: var(--text-secondary);
        }

        .loading-state, .empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 200px;
          color: var(--text-secondary);
        }

        .spinner {
          animation: spin 1s linear infinite;
          color: var(--accent-color);
          margin-bottom: 15px;
        }

        .error-card {
          padding: 12px 20px;
          display: flex;
          align-items: center;
          gap: 10px;
          color: #ff4b4b;
          background: rgba(255, 75, 75, 0.1) !important;
          border: 1px solid rgba(255, 75, 75, 0.2) !important;
        }

        .icon-accent { color: var(--accent-color); }
        .icon-success { color: #4ade80; }
        .icon-error { color: #ff4b4b; }
        .icon-dim { color: var(--text-secondary); opacity: 0.5; }
        .mb-2 { margin-bottom: 8px; }
        .mb-4 { margin-bottom: 16px; }
        .mb-6 { margin-bottom: 24px; }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        @media (max-width: 900px) {
          main { grid-template-columns: 1fr; overflow-y: auto; }
          .data-panel { overflow: visible; }
        }
      `}</style>
    </div>
  );
}

export default App;
