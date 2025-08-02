import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Dot } from 'recharts';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [selectedTurbine, setSelectedTurbine] = useState(1);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [powerCurveData, setPowerCurveData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [turbineInfo, setTurbineInfo] = useState([]);
  const [statistics, setStatistics] = useState(null);

  // Fetch turbine information and set default dates on mount
  useEffect(() => {
    fetchTurbineInfo();
    // Set default dates to a range in 2016 where we know there is data.
    setStartDate('2016-01-01');
    setEndDate('2016-03-31');
  }, []);

  // Fetch power curve and statistics when parameters change
  useEffect(() => {
    // Ensure we don't fetch until the dates are set
    if (selectedTurbine && startDate && endDate) {
      fetchPowerCurve();
      fetchStatistics();
    }
  }, [selectedTurbine, startDate, endDate]);

  const fetchTurbineInfo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/turbines/`);
      if (!response.ok) throw new Error('Failed to fetch turbine info');
      const data = await response.json();
      setTurbineInfo(data.turbines);
    } catch (err) {
      console.error('Error fetching turbine info:', err);
    }
  };

  const fetchPowerCurve = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({
        start_time: `${startDate}T00:00:00`,
        end_time: `${endDate}T23:59:59`
      });

      const response = await fetch(
        `${API_BASE_URL}/turbines/${selectedTurbine}/power-curve?${params}`
      );

      if (!response.ok) {
        // This will now trigger the user-friendly error message below
        throw new Error('API request failed');
      }

      const data = await response.json();
      // Transform data for Recharts
      const chartData = data.curve_points.map(point => ({
        windSpeed: point.wind_speed,
        power: point.average_power,
        readingCount: point.reading_count
      }));

      setPowerCurveData(chartData);
    } catch (err) {
      // --- THIS IS THE FIX ---
      // Set a more informative error message for the user.
      const friendlyError = "Dear user, the available data is from January 1, 2016, to March 31, 2016. Please select a date range within this period.";
      setError(friendlyError);
      setPowerCurveData([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchStatistics = async () => {
    try {
      const params = new URLSearchParams({
        start_time: `${startDate}T00:00:00`,
        end_time: `${endDate}T23:59:59`
      });

      const response = await fetch(
        `${API_BASE_URL}/turbines/${selectedTurbine}/statistics?${params}`
      );

      if (response.ok) {
        const data = await response.json();
        setStatistics(data);
      } else {
        setStatistics(null);
      }
    } catch (err) {
      console.error('Error fetching statistics:', err);
      setStatistics(null);
    }
  };

  // Custom dot for the chart
  const CustomDot = (props) => {
    const { cx, cy, payload } = props;
    if (payload.readingCount > 100) {
      return (
        <circle
          cx={cx}
          cy={cy}
          r={4}
          fill="#00D4FF"
          fillOpacity={0.8}
          stroke="#00D4FF"
          strokeWidth={2}
        />
      );
    }
    return null;
  };

  return (
    <div className="app">
      <div className="header">
        <h1 className="title">
          <span className="title-accent">TURBIT</span> Power Curve Analytics
        </h1>
        <p className="subtitle">Real-time Wind Turbine Performance Monitoring</p>
      </div>

      <div className="controls-container">
        <div className="control-group">
          <label className="control-label">Turbine Selection</label>
          <div className="turbine-selector">
            {turbineInfo.map(turbine => (
              <button
                key={turbine.id}
                className={`turbine-btn ${selectedTurbine === turbine.id ? 'active' : ''}`}
                onClick={() => setSelectedTurbine(turbine.id)}
              >
                <span className="turbine-name">{turbine.name}</span>
                <span className="turbine-readings">{turbine.reading_count.toLocaleString()} readings</span>
              </button>
            ))}
          </div>
        </div>

        <div className="date-controls">
          <div className="control-group">
            <label className="control-label">Start Date</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="date-input"
            />
          </div>
          <div className="control-group">
            <label className="control-label">End Date</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="date-input"
            />
          </div>
        </div>
      </div>

      {statistics && (
        <div className="stats-container">
          <div className="stat-card">
            <div className="stat-value">{statistics.avg_wind_speed?.toFixed(1)} m/s</div>
            <div className="stat-label">Avg Wind Speed</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{statistics.avg_power?.toFixed(0)} kW</div>
            <div className="stat-label">Avg Power Output</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{statistics.max_power?.toFixed(0)} kW</div>
            <div className="stat-label">Peak Power</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{statistics.count?.toLocaleString()}</div>
            <div className="stat-label">Data Points</div>
          </div>
        </div>
      )}

      <div className="chart-container">
        <h2 className="chart-title">Power Curve Visualization</h2>

        {loading && (
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>Loading power curve data...</p>
          </div>
        )}

        {error && (
          <div className="error">
            <p>{error}</p>
          </div>
        )}

        {!loading && !error && powerCurveData.length > 0 && (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart
              data={powerCurveData}
              margin={{
                top: 20,
                right: 30,
                left: 20,
                bottom: 20
              }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#1a2332" />
              <XAxis
                dataKey="windSpeed"
                stroke="#8892a6"
                label={{
                  value: 'Wind Speed (m/s)',
                  position: 'insideBottom',
                  offset: -15,
                  style: { fill: '#8892a6' }
                }}
              />
              <YAxis
                stroke="#8892a6"
                label={{
                  value: 'Power (kW)',
                  angle: -90,
                  position: 'insideLeft',
                  style: { fill: '#8892a6' }
                }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0D1221',
                  border: '1px solid #00D4FF',
                  borderRadius: '8px',
                  padding: '10px',
                }}
                itemStyle={{ color: '#00D4FF' }}
                labelStyle={{ color: '#8892a6' }}
                formatter={(value, name) => [`${value.toFixed(1)} kW`, 'Power Output']}
              />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              <Line
                type="monotone"
                dataKey="power"
                stroke="#00D4FF"
                strokeWidth={2}
                name="Power Output"
                dot={<CustomDot />}
                activeDot={{ r: 6, fill: '#00D4FF' }}
              />
            </LineChart>
          </ResponsiveContainer>
        )}

        {!loading && !error && powerCurveData.length === 0 && (
          <div className="no-data">
            <p>No data available for the selected period</p>
          </div>
        )}
      </div>

      <div className="info-section">
        <div className="info-card">
          <h3 className="info-title">Understanding Power Curves</h3>
          <p className="info-text">
            The power curve shows the relationship between wind speed and power output.
            A healthy turbine typically shows increasing power output with wind speed up to
            its rated capacity, then maintains steady output until cut-out speed.
          </p>
        </div>
        <div className="info-card">
          <h3 className="info-title">Performance Indicators</h3>
          <p className="info-text">
            Monitor deviations from expected power curves to identify potential issues
            such as blade damage, pitch system problems, or generator inefficiencies.
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
