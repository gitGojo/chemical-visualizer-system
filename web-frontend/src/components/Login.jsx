import React, { useState } from 'react';
import { setAuthToken } from '../api';

const Login = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        try {
            // Basic check is implicit in API calls later, but we set token here
            setAuthToken(username, password);
            onLogin(username);
        } catch (err) {
            setError("Invalid credentials");
        }
    };

    return (
        <div className="login-page">
            <div className="login-card">
                <h2 style={{ textAlign: 'center', marginBottom: '30px', color: 'var(--text-primary)', fontWeight: '400', letterSpacing: '2px' }}>ACCESS CONTROL</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>USERNAME</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>PASSWORD</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    {error && <p style={{ color: '#ff6b6b', textAlign: 'center', fontSize: '0.9rem' }}>{error}</p>}
                    <button type="submit" className="btn" style={{ width: '100%', marginTop: '20px' }}>AUTHENTICATE</button>
                </form>
            </div>
        </div>
    );
};

export default Login;
