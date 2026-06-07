import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios';
import { Shield, Upload, History, FileText, LogOut } from 'lucide-react';
import './style.css';

const API = 'http://localhost:8000';

const api = axios.create({
  baseURL: API,
});

function setAuth(token) {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common.Authorization;
  }
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [user, setUser] = useState(
    JSON.parse(localStorage.getItem('user') || 'null')
  );

  useEffect(() => {
    setAuth(token);
  }, [token]);

  function onLogin(data) {
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));

    setAuth(data.access_token);
    setToken(data.access_token);
    setUser(data.user);
  }

  function logout() {
    localStorage.clear();
    setAuth('');
    setToken('');
    setUser(null);
  }

  if (!token) {
    return <AuthPage onLogin={onLogin} />;
  }

  return <Dashboard user={user} logout={logout} token={token} />;
}

function AuthPage({ onLogin }) {
  const [mode, setMode] = useState('login');
  const [form, setForm] = useState({
    email: 'admin@deepguard.local',
    password: 'admin123',
    full_name: 'Admin User',
  });
  const [message, setMessage] = useState('');

  async function submit(e) {
    e.preventDefault();
    setMessage('');

    try {
      if (mode === 'register') {
        await api.post('/auth/register', form);
        setMessage(
          'Registered. You can now login. Admin role is only granted to emails in backend .env ALLOWED_ADMIN_EMAILS.'
        );
        setMode('login');
        return;
      }

      const res = await api.post('/auth/login', {
        email: form.email,
        password: form.password,
      });

      onLogin(res.data);
    } catch (err) {
      setMessage(err.response?.data?.detail || err.message);
    }
  }

  return (
    <main className="auth-page">
      <section className="card auth-card">
        <div className="brand">
          <Shield size={38} />
          <div>
            <h1>DeepGuard</h1>
            <p>Multi-modal deepfake detection starter system</p>
          </div>
        </div>

        <form onSubmit={submit} className="form">
          {mode === 'register' && (
            <input
              placeholder="Full name"
              value={form.full_name}
              onChange={(e) =>
                setForm({ ...form, full_name: e.target.value })
              }
            />
          )}

          <input
            placeholder="Email"
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />

          <input
            placeholder="Password"
            type="password"
            value={form.password}
            onChange={(e) =>
              setForm({ ...form, password: e.target.value })
            }
          />

          <button>{mode === 'login' ? 'Login' : 'Register'}</button>
        </form>

        <button
          className="link"
          onClick={() =>
            setMode(mode === 'login' ? 'register' : 'login')
          }
        >
          {mode === 'login' ? 'Create account' : 'Back to login'}
        </button>

        {message && <p className="message">{message}</p>}

        <p className="hint">
          Default first test account: register/login using
          admin@deepguard.local / admin123.
        </p>
      </section>
    </main>
  );
}

function Dashboard({ user, logout, token }) {
  const [scans, setScans] = useState([]);
  const [file, setFile] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [latest, setLatest] = useState(null);

  async function load() {
    if (!token) {
      setError('Missing login token');
      return;
    }

    try {
      const res = await api.get('/scans', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setScans(res.data);
    } catch (e) {
      setError(e.response?.data?.detail || e.message);
    }
  }

  useEffect(() => {
    if (token) {
      setAuth(token);
      load();
    }
  }, [token]);

  async function upload(e) {
    e.preventDefault();

    if (!token) {
      setError('Missing login token. Please logout and login again.');
      return;
    }

    if (!file) {
      setError('Please choose a file first.');
      return;
    }

    setBusy(true);
    setError('');

    const data = new FormData();
    data.append('file', file);

    try {
      const res = await api.post('/scans', data, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      setLatest(res.data);
      setFile(null);
      await load();
    } catch (e) {
      setError(e.response?.data?.detail || e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main>
      <header className="topbar">
        <div className="brand small">
          <Shield />
          <div>
            <h1>DeepGuard</h1>
            <p>
              {user?.email} · {user?.role}
            </p>
          </div>
        </div>

        <button className="secondary" onClick={logout}>
          <LogOut size={16} /> Logout
        </button>
      </header>

      <section className="grid">
        <div className="card">
          <h2>
            <Upload /> Analyze Media
          </h2>

          <p>
            Upload image, video, or audio. This starter package stores files on
            disk and saves metadata/results in MySQL.
          </p>

          <form onSubmit={upload} className="upload">
            <input
              type="file"
              accept=".jpg,.jpeg,.png,.mp4,.avi,.mov,.mkv,.mp3,.wav,.m4a,.flac"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <button disabled={busy}>
              {busy ? 'Analyzing...' : 'Upload and Analyze'}
            </button>
          </form>

          {error && <p className="error">{error}</p>}

          {latest && <Result scan={latest} />}
        </div>

        <div className="card">
          <h2>
            <FileText /> Project Scope
          </h2>

          <ul>
            <li>Image deepfake detection placeholder</li>
            <li>Video deepfake detection placeholder</li>
            <li>Audio deepfake recognition placeholder</li>
            <li>PDF report generation</li>
            <li>Role-based scan history</li>
          </ul>

          <p className="note">
            For final defense, replace backend/app/services/detector.py with
            trained EfficientNet-B4/video/audio model inference.
          </p>
        </div>
      </section>

      <section className="card">
        <h2>
          <History /> Scan History
        </h2>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>File</th>
                <th>Type</th>
                <th>Result</th>
                <th>Confidence</th>
                <th>Date</th>
                <th>Report</th>
              </tr>
            </thead>

            <tbody>
              {scans.map((s) => (
                <tr key={s.id}>
                  <td>{s.id}</td>
                  <td>{s.original_filename}</td>
                  <td>{s.modality}</td>
                  <td>
                    <span
                      className={
                        s.prediction === 'Fake' ? 'badge fake' : 'badge real'
                      }
                    >
                      {s.prediction}
                    </span>
                  </td>
                  <td>{s.confidence}%</td>
                  <td>{new Date(s.created_at).toLocaleString()}</td>
                  <td>
                    <a href={`${API}${s.report_url}`} target="_blank">
                      PDF
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}

function Result({ scan }) {
  return (
    <div className="result">
      <h3>Latest Result</h3>
      <p>
        <b>{scan.original_filename}</b>
      </p>
      <p>
        <span
          className={scan.prediction === 'Fake' ? 'badge fake' : 'badge real'}
        >
          {scan.prediction}
        </span>{' '}
        Confidence: <b>{scan.confidence}%</b>
      </p>
      <p>{scan.explanation}</p>
      <a href={`${API}${scan.report_url}`} target="_blank">
        Download PDF Report
      </a>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
