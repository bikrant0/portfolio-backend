import { useState, useEffect } from "react";
import { fetchHealth } from '../services/api';
import './Navbar.css';

export default function Navabar(){
    const [heatlthStatus, setHealthStatus] = useState('Loading');
    const [latency, setLatency] = useState(0);

    useEffect(() => {
        const checkHealth = async () => {
            const startTime = Date.now();
            try {
                const response = await fetch('http://127.0.0.1:8000/api/v1/health/');
                if (response.ok) {
                    setHealthStatus('healthy');
                    setLatency(Date.now() - startTime);
                } else {
                    setHealthStatus('error');
                }
            } catch (error) {
                setHealthStatus('error');
            }
        };

        checkHealth();
        const interval = setInterval(checkHealth, 15000);
        return () => clearInterval(interval);
    }, []);

    return(
        <nav className="navbar">
            <div className="navbar-brand">PORTFOLIO</div>
            <div className="nav-links">
                <span>Home</span>
                <span>Projects</span>
                <span style={{ cursor: 'pointer' }}>Playground</span>
            </div>
            <div className="live-ledger">
                <span className={'status-dot ${healthStatus}'}>●</span>
                <span className="ledger-text">
                    { healthStatus === 'healthy' ? `200 ● ${latency}ms` : 'Offline'}
                </span>
            </div>
        </nav>
    )

}