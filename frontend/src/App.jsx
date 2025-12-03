import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [projectConfig, setProjectConfig] = useState({
    project_name: 'my_test_project',
    repository_path: '',
    repository_type: 'local',
    document_paths: []
  });
  
  const [workflowStatus, setWorkflowStatus] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState(null);
  const [outputFiles, setOutputFiles] = useState([]);
  const [configCheck, setConfigCheck] = useState(null);
  const [error, setError] = useState(null);

  // Check configuration on mount
  useEffect(() => {
    checkConfiguration();
  }, []);

  // Poll status when workflow is running
  useEffect(() => {
    let interval;
    if (isRunning) {
      interval = setInterval(() => {
        fetchStatus();
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  const checkConfiguration = async () => {
    try {
      const response = await axios.get('/api/config/check');
      setConfigCheck(response.data);
      if (!response.data.all_valid) {
        setError('Configuration incomplete. Please check your .env file.');
      }
    } catch (err) {
      setError('Failed to check configuration');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProjectConfig(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleDocPathsChange = (e) => {
    const paths = e.target.value.split(',').map(p => p.trim()).filter(p => p);
    setProjectConfig(prev => ({
      ...prev,
      document_paths: paths
    }));
  };

  const startProject = async () => {
    setError(null);
    try {
      const response = await axios.post('/api/project/start', projectConfig);
      setIsRunning(true);
      setWorkflowStatus({
        status: 'started',
        message: 'Initializing...',
        progress: 0
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start project');
    }
  };

  const fetchStatus = async () => {
    try {
      const response = await axios.get('/api/project/status');
      setWorkflowStatus(response.data);
      
      if (response.data.status === 'completed') {
        setIsRunning(false);
        fetchResults();
        fetchOutputFiles();
      } else if (response.data.status === 'failed') {
        setIsRunning(false);
        setError(response.data.message);
      }
    } catch (err) {
      console.error('Failed to fetch status', err);
    }
  };

  const fetchResults = async () => {
    try {
      const response = await axios.get('/api/project/results');
      setResults(response.data);
    } catch (err) {
      console.error('Failed to fetch results', err);
    }
  };

  const fetchOutputFiles = async () => {
    try {
      const response = await axios.get('/api/files/list');
      setOutputFiles(response.data.files || []);
    } catch (err) {
      console.error('Failed to fetch files', err);
    }
  };

  const downloadFile = async (filePath) => {
    try {
      const response = await axios.get(`/api/files/download/${filePath}`);
      const blob = new Blob([response.data.content], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = response.data.filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to download file');
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>🤖 MASTT - Multi-Agent Software Testing Team</h1>
          <p>Your Code, Anchored in Quality</p>
        </header>

        {/* Configuration Check */}
        {configCheck && !configCheck.all_valid && (
          <div className="alert alert-error">
            <strong>Configuration Issues:</strong>
            <ul>
              {!configCheck.google_api_key && <li>Google API Key not configured</li>}
              {parseFloat(configCheck.python_version) < 3.9 && <li>Python 3.9+ required</li>}
            </ul>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {/* Project Configuration Form */}
        {!isRunning && !results && (
          <div className="card">
            <h2>📋 Project Configuration</h2>
            <form onSubmit={(e) => { e.preventDefault(); startProject(); }}>
              <div className="form-group">
                <label>Project Name:</label>
                <input
                  type="text"
                  name="project_name"
                  value={projectConfig.project_name}
                  onChange={handleInputChange}
                  placeholder="my_test_project"
                  required
                />
              </div>

              <div className="form-group">
                <label>Repository Type:</label>
                <select
                  name="repository_type"
                  value={projectConfig.repository_type}
                  onChange={handleInputChange}
                >
                  <option value="local">Local Path</option>
                  <option value="github">GitHub URL</option>
                </select>
              </div>

              <div className="form-group">
                <label>Repository Path/URL:</label>
                <input
                  type="text"
                  name="repository_path"
                  value={projectConfig.repository_path}
                  onChange={handleInputChange}
                  placeholder="/path/to/code or https://github.com/user/repo"
                  required
                />
              </div>

              <div className="form-group">
                <label>Document Paths (comma-separated):</label>
                <input
                  type="text"
                  value={projectConfig.document_paths.join(', ')}
                  onChange={handleDocPathsChange}
                  placeholder="./docs, ./requirements"
                />
              </div>

              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={!configCheck?.all_valid}
              >
                🚀 Start Project
              </button>
            </form>
          </div>
        )}

        {/* Workflow Progress */}
        {isRunning && workflowStatus && (
          <div className="card">
            <h2>⚙️ Workflow Progress</h2>
            <div className="progress-container">
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ width: `${workflowStatus.progress}%` }}
                ></div>
              </div>
              <div className="progress-info">
                <span className="progress-text">{workflowStatus.progress}%</span>
                <span className="phase-text">{workflowStatus.current_phase}</span>
              </div>
              <p className="status-message">{workflowStatus.message}</p>
            </div>
            
            <div className="phases">
              <div className={`phase ${workflowStatus.progress >= 20 ? 'completed' : ''}`}>
                📊 Code Analysis
              </div>
              <div className={`phase ${workflowStatus.progress >= 30 ? 'completed' : ''}`}>
                📄 Document Processing
              </div>
              <div className={`phase ${workflowStatus.progress >= 45 ? 'completed' : ''}`}>
                📝 Test Planning
              </div>
              <div className={`phase ${workflowStatus.progress >= 60 ? 'completed' : ''}`}>
                ✍️ Test Case Writing
              </div>
              <div className={`phase ${workflowStatus.progress >= 75 ? 'completed' : ''}`}>
                🤖 Automation Code Generation
              </div>
              <div className={`phase ${workflowStatus.progress >= 90 ? 'completed' : ''}`}>
                📚 Documentation
              </div>
              <div className={`phase ${workflowStatus.progress === 100 ? 'completed' : ''}`}>
                ✅ Complete
              </div>
            </div>
          </div>
        )}

        {/* Results Display */}
        {results && (
          <div className="card">
            <h2>✅ Project Complete!</h2>
            <div className="results-grid">
              <div className={`result-item ${results.test_plan ? 'success' : 'pending'}`}>
                📋 Test Plan
              </div>
              <div className={`result-item ${results.test_cases ? 'success' : 'pending'}`}>
                ✍️ Test Cases
              </div>
              <div className={`result-item ${results.automation_framework ? 'success' : 'pending'}`}>
                🏗️ Automation Framework
              </div>
              <div className={`result-item ${results.api_automation ? 'success' : 'pending'}`}>
                🔌 API Tests
              </div>
              <div className={`result-item ${results.db_automation ? 'success' : 'pending'}`}>
                🗄️ Database Tests
              </div>
              <div className={`result-item ${results.cli_automation ? 'success' : 'pending'}`}>
                💻 CLI Tests
              </div>
              <div className={`result-item ${results.gui_automation ? 'success' : 'pending'}`}>
                🖥️ GUI Tests
              </div>
              <div className={`result-item ${results.documentation ? 'success' : 'pending'}`}>
                📚 Documentation
              </div>
            </div>
            
            <div className="output-info">
              <p><strong>Output Directory:</strong> {results.output_directory}</p>
            </div>

            <button 
              className="btn btn-secondary"
              onClick={() => {
                setResults(null);
                setWorkflowStatus(null);
                setOutputFiles([]);
              }}
            >
              Start New Project
            </button>
          </div>
        )}

        {/* Output Files */}
        {outputFiles.length > 0 && (
          <div className="card">
            <h2>📁 Generated Files ({outputFiles.length})</h2>
            <div className="files-list">
              {outputFiles.map((file, index) => (
                <div key={index} className="file-item">
                  <span className="file-name">{file.path}</span>
                  <button 
                    className="btn btn-sm"
                    onClick={() => downloadFile(file.path)}
                  >
                    ⬇️ Download
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        <footer className="footer">
          <p>Powered by Google ADK & Gemini AI</p>
        </footer>
      </div>
    </div>
  );
}

export default App;