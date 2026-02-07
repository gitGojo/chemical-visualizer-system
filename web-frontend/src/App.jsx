import React, { useState } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
    const [user, setUser] = useState(null);

    return (
        <div className="App">
            {!user ? (
                <Login onLogin={setUser} />
            ) : (
                <Dashboard />
            )}
        </div>
    );
}

export default App;
