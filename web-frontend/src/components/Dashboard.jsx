import React, { useState, useEffect } from 'react';
import api from '../api';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

const Dashboard = () => {
    const [summary, setSummary] = useState(null);
    const [dataLoaded, setDataLoaded] = useState(false);
    const [history, setHistory] = useState([]);
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [uploadMsg, setUploadMsg] = useState('');

    const fetchHistory = async () => {
        try {
            const histRes = await api.get('history/');
            setHistory(histRes.data);
        } catch (error) {
            console.error("Error fetching history", error);
        }
    };

    const fetchSummary = async () => {
        try {
            const sumRes = await api.get('summary/');
            setSummary(sumRes.data);
        } catch (error) {
            console.error("Error fetching summary", error);
        }
    };

    useEffect(() => {
        fetchHistory();
        // Do NOT fetch summary on mount, per user request.
    }, []);

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);
        setLoading(true);
        setUploadMsg('');

        try {
            await api.post('upload/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setUploadMsg('Upload successful!');
            setFile(null);
            setDataLoaded(true);
            fetchSummary(); // NOW we show the charts
            fetchHistory(); // Update history list
        } catch (error) {
            const apiError = error.response?.data?.error || error.message;
            setUploadMsg(`Upload failed: ${apiError}`);
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadReport = async () => {
        try {
            const response = await api.get('report_pdf/', { responseType: 'blob' });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'summary_report.pdf');
            document.body.appendChild(link);
            link.click();
        } catch (error) {
            console.error("Error downloading report", error);
        }
    };

    // Chart Global Defaults for Dark Tech Theme
    ChartJS.defaults.color = '#a0a0a0';
    ChartJS.defaults.borderColor = '#222';
    ChartJS.defaults.scale.grid.color = '#222';

    // Chart Data Preparation
    const barData = summary ? {
        labels: ['Avg Flowrate', 'Avg Pressure', 'Avg Temp'],
        datasets: [{
            label: 'Average Parameters',
            data: [summary.avg_flowrate, summary.avg_pressure, summary.avg_temperature],
            backgroundColor: 'rgba(179, 0, 0, 0.4)', // Darker red fill
            borderColor: '#b30000', // Darker red border
            borderWidth: 2,
            hoverBackgroundColor: 'rgba(179, 0, 0, 0.6)',
        }]
    } : null;

    const pieData = summary && summary.type_distribution ? {
        labels: Object.keys(summary.type_distribution),
        datasets: [{
            data: Object.values(summary.type_distribution),
            backgroundColor: [
                'rgba(179, 0, 0, 0.8)',    // Base Dark Red
                'rgba(140, 0, 0, 0.8)',    // Deep Red
                'rgba(100, 0, 0, 0.8)',    // Very Dark Red
                'rgba(220, 20, 60, 0.8)',  // Crimson
                'rgba(128, 0, 0, 0.8)',    // Maroon
            ],
            borderColor: '#121212', // Match card bg
            borderWidth: 2,
        }]
    } : null;

    return (
        <div className="container">
            <div className="header">
                <h1>Chemical Visualizer Dashboard</h1>
                <button className="btn btn-primary" onClick={handleDownloadReport} disabled={!summary}>
                    Download PDF Report
                </button>
            </div>

            {/* Upload Section */}
            <div className="card">
                <h3>Upload Dataset</h3>
                <form onSubmit={handleUpload} style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                    <input type="file" accept=".csv" onChange={e => setFile(e.target.files[0])} />
                    <button type="submit" className="btn btn-primary" disabled={!file || loading}>
                        {loading ? 'Uploading...' : 'Upload CSV'}
                    </button>
                    <span>{uploadMsg}</span>
                </form>
            </div>

            {dataLoaded && summary && summary.id ? (
                <>
                    {/* Key Metrics */}
                    <div className="card" style={{ display: 'flex', justifyContent: 'space-around' }}>
                        <div><strong>Total Equipment:</strong> {summary.total_equipment}</div>
                        <div><strong>Avg Flow:</strong> {summary.avg_flowrate?.toFixed(2)}</div>
                        <div><strong>Avg Pressure:</strong> {summary.avg_pressure?.toFixed(2)}</div>
                        <div><strong>Avg Temp:</strong> {summary.avg_temperature?.toFixed(2)}</div>
                    </div>

                    {/* Charts */}
                    <div className="charts-grid">
                        <div className="card">
                            <h3>Average Parameters</h3>
                            {barData && <Bar data={barData} />}
                        </div>
                        <div className="card">
                            <h3>Equipment Distribution</h3>
                            {pieData && <Pie data={pieData} />}
                        </div>
                    </div>
                </>
            ) : (
                <div className="placeholder-card">
                    <h2>Analytics Unavailable</h2>
                    <p>Upload a CSV file to generate charts and insights.</p>
                </div>
            )}

            {/* History Table */}
            <div className="card">
                <h3>Upload History (Last 5)</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Dataset ID</th>
                            <th>Uploaded At</th>
                            <th>Total Equipment</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.map(item => (
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{new Date(item.uploaded_at).toLocaleString()}</td>
                                <td>{item.total_equipment}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div >
    );
};

export default Dashboard;
