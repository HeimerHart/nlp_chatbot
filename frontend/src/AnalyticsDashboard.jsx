import { useEffect, useState } from "react";
import api from "./api";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
  ResponsiveContainer,
} from "recharts";

const GRID_COLOR = "rgba(255,255,255,0.08)";
const AXIS_COLOR = "#5c5c60";
const ACCENT = "#f2f2f0";

const tooltipStyle = {
  background: "#191919",
  border: "1px solid rgba(255,255,255,0.12)",
  borderRadius: 10,
  fontSize: 12.5,
  color: "#f2f2f0",
};

function AnalyticsDashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [error, setError] = useState(false);

  const loadAnalytics = async () => {
    setError(false);
    try {
      const response = await api.get("/api/analytics");
      setAnalytics(response.data);
    } catch (err) {
      console.log(err);
      setError(true);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  if (error) {
    return (
      <div className="admin-card admin-empty">
        Couldn't load analytics.{" "}
        <button className="text-btn" onClick={loadAnalytics}>
          Retry
        </button>
      </div>
    );
  }

  const lineData = analytics
    ? Object.entries(analytics.queries_per_day).map(([date, count]) => ({
        date,
        count,
      }))
    : [];

  const barData = analytics
    ? analytics.top_intents.map((intent) => ({
        intent: intent[0],
        count: intent[1],
      }))
    : [];

  if (!analytics) {
    return <div className="admin-card admin-empty">Loading analytics…</div>;
  }

  return (
    <div className="analytics-grid">
      <div className="stat-tile">
        <span className="stat-label">Total conversations</span>
        <span className="stat-value">{analytics.total_conversations}</span>
      </div>
      <div className="stat-tile">
        <span className="stat-label">Active users</span>
        <span className="stat-value">{analytics.active_users}</span>
      </div>
      <div className="stat-tile">
        <span className="stat-label">Unresolved rate</span>
        <span className="stat-value">{analytics.unresolved_rate.toFixed(1)}%</span>
      </div>

      <div className="chart-card">
        <h3>Queries per day</h3>
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={lineData}>
            <CartesianGrid stroke={GRID_COLOR} vertical={false} />
            <XAxis dataKey="date" stroke={AXIS_COLOR} fontSize={11} tickLine={false} />
            <YAxis stroke={AXIS_COLOR} fontSize={11} tickLine={false} allowDecimals={false} />
            <Tooltip contentStyle={tooltipStyle} />
            <Line type="monotone" dataKey="count" stroke={ACCENT} strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-card">
        <h3>Top 5 intents</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={barData}>
            <CartesianGrid stroke={GRID_COLOR} vertical={false} />
            <XAxis dataKey="intent" stroke={AXIS_COLOR} fontSize={11} tickLine={false} />
            <YAxis stroke={AXIS_COLOR} fontSize={11} tickLine={false} allowDecimals={false} />
            <Tooltip contentStyle={tooltipStyle} />
            <Bar dataKey="count" fill={ACCENT} radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default AnalyticsDashboard;
