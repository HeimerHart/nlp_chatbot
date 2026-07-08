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
    Bar
} from "recharts";

function AnalyticsDashboard() {

    const [analytics, setAnalytics] = useState(null);

    useEffect(() => {
        loadAnalytics();
    }, []);

    const loadAnalytics = async () => {

        const response = await api.get(
            "/api/analytics"
        );

        setAnalytics(response.data);
    };

    const lineData = analytics
        ? Object.entries(
              analytics.queries_per_day
          ).map(([date, count]) => ({
              date,
              count
          }))
        : [];

    const barData = analytics
        ? analytics.top_intents.map((intent) => ({
              intent: intent[0],
              count: intent[1]
          }))
        : [];

    if (!analytics) {
        return <h2>Loading...</h2>;
    }

    return (
        <div style={{ padding: "20px" }}>

            <h1>Analytics Dashboard</h1>

            <hr />

            <h2>
                Total Conversations : {analytics.total_conversations}
            </h2>

            <h2>
                Active Users : {analytics.active_users}
            </h2>

            <h2>
                Unresolved Rate : {analytics.unresolved_rate.toFixed(2)}%
            </h2>

            <hr />

            <h2>Queries Per Day</h2>

            <LineChart
                width={700}
                height={300}
                data={lineData}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line
                    type="monotone"
                    dataKey="count"
                />
            </LineChart>

            <hr />

            <h2>Top 5 Intents</h2>

            <BarChart
                width={700}
                height={300}
                data={barData}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="intent" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" />
            </BarChart>

        </div>
    );
}

export default AnalyticsDashboard;