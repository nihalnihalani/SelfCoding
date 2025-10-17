import { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { motion, useInView, useMotionValue, useSpring, animate } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { SkeletonMetricCard, SkeletonChart } from './ui/skeleton';
import { Target, TrendingUp, Database, AlertCircle, ArrowUp, ArrowDown, Minus } from 'lucide-react';
import { toast } from '../lib/toast-config';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Animated counter component
const AnimatedCounter = ({ value, decimals = 0, suffix = '' }) => {
  const ref = useRef(null);
  const motionValue = useMotionValue(0);
  const springValue = useSpring(motionValue, { duration: 2000 });
  const isInView = useInView(ref, { once: true });

  useEffect(() => {
    if (isInView) {
      animate(motionValue, value, { duration: 2 });
    }
  }, [motionValue, isInView, value]);

  useEffect(() => {
    springValue.on('change', (latest) => {
      if (ref.current) {
        ref.current.textContent = latest.toFixed(decimals) + suffix;
      }
    });
  }, [springValue, decimals, suffix]);

  return <span ref={ref}>0{suffix}</span>;
};

// Sparkline component
const Sparkline = ({ data, color = '#6366f1' }) => {
  if (!data || data.length === 0) return null;
  
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  
  const points = data.map((value, index) => {
    const x = (index / (data.length - 1)) * 100;
    const y = 100 - ((value - min) / range) * 100;
    return `${x},${y}`;
  }).join(' ');

  return (
    <svg className="w-full h-8" viewBox="0 0 100 100" preserveAspectRatio="none">
      <polyline
        points={points}
        fill="none"
        stroke={color}
        strokeWidth="2"
        vectorEffect="non-scaling-stroke"
      />
    </svg>
  );
};

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [previousMetrics, setPreviousMetrics] = useState(null);

  useEffect(() => {
    loadMetrics();
    const interval = setInterval(loadMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadMetrics = async () => {
    try {
      const response = await axios.get(`${API}/metrics`);
      if (metrics) {
        setPreviousMetrics(metrics);
      }
      setMetrics(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load metrics:', error);
      toast.error('Failed to load metrics');
      setLoading(false);
    }
  };

  const getTrend = (current, previous) => {
    if (!previous) return 'neutral';
    if (current > previous) return 'up';
    if (current < previous) return 'down';
    return 'neutral';
  };

  const getTrendPercentage = (current, previous) => {
    if (!previous || previous === 0) return 0;
    return ((current - previous) / previous) * 100;
  };

  if (loading) {
    return (
      <div data-testid="loading-metrics" className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold text-slate-800 dark:text-slate-200 mb-2">📊 Learning Dashboard</h2>
          <p className="text-slate-600 dark:text-slate-400">Track the AI agent's improvement over time</p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <SkeletonMetricCard key={i} />
          ))}
        </div>
        <SkeletonChart />
      </div>
    );
  }

  if (!metrics) {
    return (
      <div data-testid="no-metrics" className="text-center py-20">
        <div className="text-6xl mb-4">📊</div>
        <p className="text-slate-600 dark:text-slate-400 text-lg">No metrics available</p>
        <p className="text-slate-500 dark:text-slate-500 text-sm mt-2">Generate some apps to see your dashboard!</p>
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
          previousValue={previousMetrics?.total_apps}
          icon={<Target className="w-5 h-5" />}
          color="from-blue-500 to-blue-600"
          testId="metric-apps-built"
          sparklineData={metrics.success_history?.slice(-10).map((_, i) => i + 1)}
          sparklineColor="#3b82f6"
        />
        <MetricCard
          title="Success Rate"
          value={metrics.success_rate * 100}
          previousValue={previousMetrics?.success_rate * 100}
          suffix="%"
          decimals={1}
          icon={<TrendingUp className="w-5 h-5" />}
          color="from-green-500 to-green-600"
          testId="metric-success-rate"
          sparklineData={metrics.success_history?.slice(-10).map(r => r * 100)}
          sparklineColor="#22c55e"
        />
        <MetricCard
          title="Learned Patterns"
          value={metrics.pattern_count}
          previousValue={previousMetrics?.pattern_count}
          icon={<Database className="w-5 h-5" />}
          color="from-purple-500 to-purple-600"
          testId="metric-patterns"
          sparklineData={metrics.success_history?.slice(-10).map((_, i) => Math.min(i * 2, metrics.pattern_count))}
          sparklineColor="#a855f7"
        />
        <MetricCard
          title="Failures"
          value={metrics.failed_attempts}
          previousValue={previousMetrics?.failed_attempts}
          icon={<AlertCircle className="w-5 h-5" />}
          color="from-red-500 to-red-600"
          testId="metric-failures"
          invertTrend={true}
          sparklineData={metrics.success_history?.slice(-10).map((_, i) => Math.max(0, 5 - i))}
          sparklineColor="#ef4444"
        />
      </div>

      {/* Success Rate Chart */}
      {metrics.success_history.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card className="border-slate-200 dark:border-slate-700 shadow-lg">
            <CardHeader>
              <CardTitle className="text-xl">Learning Progress</CardTitle>
              <CardDescription>Success rate over recent generations</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart
                  data={metrics.success_history.slice(-20).map((rate, index) => ({
                    generation: index + 1,
                    successRate: rate * 100,
                  }))}
                  margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                >
                  <defs>
                    <linearGradient id="colorSuccess" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#22c55e" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#22c55e" stopOpacity={0.1}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-slate-200 dark:stroke-slate-700" />
                  <XAxis 
                    dataKey="generation" 
                    label={{ value: 'Generation', position: 'insideBottom', offset: -5 }}
                    className="text-slate-600 dark:text-slate-400"
                  />
                  <YAxis 
                    label={{ value: 'Success Rate (%)', angle: -90, position: 'insideLeft' }}
                    domain={[0, 100]}
                    className="text-slate-600 dark:text-slate-400"
                  />
                  <RechartsTooltip
                    contentStyle={{
                      backgroundColor: 'hsl(var(--card))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px',
                      color: 'hsl(var(--card-foreground))'
                    }}
                    formatter={(value) => [`${value.toFixed(1)}%`, 'Success Rate']}
                    labelFormatter={(label) => `Generation ${label}`}
                  />
                  <Area
                    type="monotone"
                    dataKey="successRate"
                    stroke="#22c55e"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorSuccess)"
                    animationDuration={1500}
                  />
                </AreaChart>
              </ResponsiveContainer>
              <p className="text-sm text-slate-600 dark:text-slate-400 mt-4 text-center font-medium">
                📈 Agent improving over time!
              </p>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Insights */}
      {metrics.total_apps > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card className="border-indigo-200 dark:border-indigo-800 bg-indigo-50/50 dark:bg-indigo-900/20">
            <CardHeader>
              <CardTitle className="text-xl flex items-center space-x-2">
                <motion.span
                  animate={{ rotate: [0, 10, -10, 0] }}
                  transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
                >
                  💡
                </motion.span>
                <span>Insights</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {metrics.success_rate >= 0.8 && (
                  <motion.li
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 }}
                    className="flex items-start space-x-3 p-3 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800"
                  >
                    <span className="text-green-600 dark:text-green-400 text-xl">✅</span>
                    <span className="text-slate-700 dark:text-slate-300 flex-1">
                      Excellent success rate! The agent is performing very well.
                    </span>
                  </motion.li>
                )}
                {metrics.pattern_count > 5 && (
                  <motion.li
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 }}
                    className="flex items-start space-x-3 p-3 rounded-lg bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800"
                  >
                    <span className="text-purple-600 dark:text-purple-400 text-xl">📚</span>
                    <span className="text-slate-700 dark:text-slate-300 flex-1">
                      Building a rich pattern library with {metrics.pattern_count} patterns.
                    </span>
                  </motion.li>
                )}
                {metrics.success_history.length > 1 && 
                 metrics.success_history[metrics.success_history.length - 1] > 
                 metrics.success_history[0] && (
                  <motion.li
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 }}
                    className="flex items-start space-x-3 p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800"
                  >
                    <span className="text-blue-600 dark:text-blue-400 text-xl">📈</span>
                    <span className="text-slate-700 dark:text-slate-300 flex-1">
                      Success rate is improving! The agent is learning from experience.
                    </span>
                  </motion.li>
                )}
                {metrics.total_apps < 5 && (
                  <motion.li
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 }}
                    className="flex items-start space-x-3 p-3 rounded-lg bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800"
                  >
                    <span className="text-yellow-600 dark:text-yellow-400 text-xl">👶</span>
                    <span className="text-slate-700 dark:text-slate-300 flex-1">
                      Just getting started! Generate more apps to see learning in action.
                    </span>
                  </motion.li>
                )}
              </ul>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
};

const MetricCard = ({ 
  title, 
  value, 
  previousValue,
  suffix = '', 
  decimals = 0,
  icon, 
  color, 
  testId,
  invertTrend = false,
  sparklineData,
  sparklineColor
}) => {
  // Define helper functions first
  const getTrend = (current, previous) => {
    if (!previous) return 'neutral';
    if (current > previous) return 'up';
    if (current < previous) return 'down';
    return 'neutral';
  };

  const getTrendPercentage = (current, previous) => {
    if (!previous || previous === 0) return 0;
    return ((current - previous) / previous) * 100;
  };

  // Now use them
  const trend = previousValue !== undefined ? getTrend(value, previousValue) : 'neutral';
  const trendPercentage = previousValue !== undefined ? getTrendPercentage(value, previousValue) : 0;
  
  const getTrendIcon = () => {
    if (trend === 'neutral') return <Minus className="w-4 h-4" />;
    if (trend === 'up') return <ArrowUp className="w-4 h-4" />;
    return <ArrowDown className="w-4 h-4" />;
  };

  const getTrendColor = () => {
    if (trend === 'neutral') return 'text-slate-500';
    const isPositive = invertTrend ? trend === 'down' : trend === 'up';
    return isPositive ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
    >
      <Card 
        data-testid={testId} 
        className="border-slate-200 dark:border-slate-700 shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden group"
      >
        <motion.div 
          className={`h-2 bg-gradient-to-r ${color}`}
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        />
        <CardContent className="pt-6">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm font-medium text-slate-600 dark:text-slate-400">{title}</p>
            <div className="text-slate-400 dark:text-slate-500 group-hover:scale-110 transition-transform">
              {icon}
            </div>
          </div>
          
          <div className="flex items-baseline space-x-2 mb-2">
            <p className="text-3xl font-bold text-slate-800 dark:text-slate-200">
              <AnimatedCounter value={value} decimals={decimals} suffix={suffix} />
            </p>
            {trend !== 'neutral' && (
              <motion.div
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5 }}
                className={`flex items-center space-x-1 text-sm font-medium ${getTrendColor()}`}
              >
                {getTrendIcon()}
                <span>{Math.abs(trendPercentage).toFixed(1)}%</span>
              </motion.div>
            )}
          </div>

          {sparklineData && sparklineData.length > 0 && (
            <div className="mt-3 opacity-60 group-hover:opacity-100 transition-opacity">
              <Sparkline data={sparklineData} color={sparklineColor} />
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default Dashboard;