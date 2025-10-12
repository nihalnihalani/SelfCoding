import { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Target, TrendingUp, Database, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMetrics();
    const interval = setInterval(loadMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadMetrics = async () => {
    try {
      const response = await axios.get(`${API}/metrics`);
      setMetrics(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load metrics:', error);
      toast.error('Failed to load metrics');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div data-testid="loading-metrics" className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading metrics...</p>
        </div>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div data-testid="no-metrics" className="text-center py-20">
        <p className="text-slate-600">No metrics available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6" data-testid="dashboard-container">
      <div>
        <h2 className="text-3xl font-bold text-slate-800 mb-2">📊 Learning Dashboard</h2>
        <p className="text-slate-600">Track the AI agent's improvement over time</p>
      </div>
      
      {/* Metrics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard
          title="Apps Built"
          value={metrics.total_apps}
          icon={<Target className="w-5 h-5" />}
          color="from-blue-500 to-blue-600"
          testId="metric-apps-built"
        />
        <MetricCard
          title="Success Rate"
          value={`${(metrics.success_rate * 100).toFixed(1)}%`}
          icon={<TrendingUp className="w-5 h-5" />}
          color="from-green-500 to-green-600"
          testId="metric-success-rate"
        />
        <MetricCard
          title="Learned Patterns"
          value={metrics.pattern_count}
          icon={<Database className="w-5 h-5" />}
          color="from-purple-500 to-purple-600"
          testId="metric-patterns"
        />
        <MetricCard
          title="Failures"
          value={metrics.failed_attempts}
          icon={<AlertCircle className="w-5 h-5" />}
          color="from-red-500 to-red-600"
          testId="metric-failures"
        />
      </div>

      {/* Success Rate Chart */}
      {metrics.success_history.length > 0 && (
        <Card className="border-slate-200 shadow-lg">
          <CardHeader>
            <CardTitle className="text-xl">Learning Progress</CardTitle>
            <CardDescription>Success rate over recent generations (5-generation rolling average)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-end justify-between space-x-2">
              {metrics.success_history.slice(-20).map((rate, index) => (
                <div
                  key={index}
                  data-testid={`chart-bar-${index}`}
                  className="flex-1 bg-gradient-to-t from-green-500 to-green-400 rounded-t-lg relative group transition-all duration-200 hover:opacity-80"
                  style={{ height: `${rate * 100}%`, minHeight: '4px' }}
                >
                  <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-slate-900 text-white text-xs py-1 px-2 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                    Gen {index + 1}: {(rate * 100).toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-6 flex justify-between text-xs text-slate-500">
              <span>Generation #1</span>
              <span>Latest</span>
            </div>
            <p className="text-sm text-slate-600 mt-4 text-center font-medium">
              📈 Agent improving over time!
            </p>
          </CardContent>
        </Card>
      )}

      {/* Insights */}
      {metrics.total_apps > 0 && (
        <Card className="border-indigo-200 bg-indigo-50/50">
          <CardHeader>
            <CardTitle className="text-xl flex items-center space-x-2">
              <span>💡</span>
              <span>Insights</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-slate-700">
              {metrics.success_rate >= 0.8 && (
                <li className="flex items-center space-x-2">
                  <span className="text-green-600">✅</span>
                  <span>Excellent success rate! The agent is performing very well.</span>
                </li>
              )}
              {metrics.pattern_count > 5 && (
                <li className="flex items-center space-x-2">
                  <span className="text-purple-600">📚</span>
                  <span>Building a rich pattern library with {metrics.pattern_count} patterns.</span>
                </li>
              )}
              {metrics.success_history.length > 1 && 
               metrics.success_history[metrics.success_history.length - 1] > 
               metrics.success_history[0] && (
                <li className="flex items-center space-x-2">
                  <span className="text-blue-600">📈</span>
                  <span>Success rate is improving! The agent is learning from experience.</span>
                </li>
              )}
              {metrics.total_apps < 5 && (
                <li className="flex items-center space-x-2">
                  <span className="text-yellow-600">👶</span>
                  <span>Just getting started! Generate more apps to see learning in action.</span>
                </li>
              )}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

const MetricCard = ({ title, value, icon, color, testId }) => (
  <Card data-testid={testId} className="border-slate-200 shadow-md overflow-hidden">
    <div className={`h-2 bg-gradient-to-r ${color}`}></div>
    <CardContent className="pt-6">
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm font-medium text-slate-600">{title}</p>
        <div className="text-slate-400">{icon}</div>
      </div>
      <p className="text-3xl font-bold text-slate-800">{value}</p>
    </CardContent>
  </Card>
);

export default Dashboard;