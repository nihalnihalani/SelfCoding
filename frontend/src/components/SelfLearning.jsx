import { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Brain, TrendingUp, Database, Lightbulb, RefreshCw, BookOpen } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SelfLearning = () => {
  const [learningReport, setLearningReport] = useState(null);
  const [memoryStats, setMemoryStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLearningData();
    const interval = setInterval(loadLearningData, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadLearningData = async () => {
    try {
      const [reportRes, memoryRes] = await Promise.all([
        axios.get(`${API}/self-learning/report`),
        axios.get(`${API}/self-learning/memory`)
      ]);
      
      setLearningReport(reportRes.data);
      setMemoryStats(memoryRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load learning data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div data-testid="loading-self-learning" className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading self-learning system...</p>
        </div>
      </div>
    );
  }

  const efficiency = learningReport?.learning_efficiency || {};
  const stats = memoryStats?.statistics || {};
  const knowledge = memoryStats?.consolidated_knowledge || {};

  return (
    <div className="space-y-6" data-testid="self-learning-container">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-800 mb-2 flex items-center space-x-3">
            <Brain className="h-8 w-8 text-indigo-600" />
            <span>Self-Learning System</span>
          </h2>
          <p className="text-slate-600">Recursive self-improvement with Reflexion framework</p>
        </div>
        <Button
          onClick={loadLearningData}
          variant="outline"
          className="flex items-center space-x-2"
        >
          <RefreshCw className="h-4 w-4" />
          <span>Refresh</span>
        </Button>
      </div>

      {/* Learning Efficiency */}
      {efficiency.status !== 'insufficient_data' && (
        <Card className={`border-2 ${efficiency.status === 'improving' ? 'border-green-300 bg-green-50' : 'border-orange-300 bg-orange-50'}`}>
          <CardHeader>
            <CardTitle className="text-xl flex items-center space-x-2">
              <TrendingUp className="h-5 w-5" />
              <span>Learning Efficiency</span>
            </CardTitle>
            <CardDescription>
              {efficiency.status === 'improving' ? 
                '✅ System is improving over time' : 
                '⚠️ Performance needs attention'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-white rounded-lg">
                <p className="text-sm text-slate-600 mb-1">Early Average</p>
                <p className="text-2xl font-bold text-slate-800">
                  {efficiency.early_average?.toFixed(1)}
                </p>
              </div>
              <div className="text-center p-4 bg-white rounded-lg">
                <p className="text-sm text-slate-600 mb-1">Recent Average</p>
                <p className="text-2xl font-bold text-slate-800">
                  {efficiency.recent_average?.toFixed(1)}
                </p>
              </div>
              <div className="text-center p-4 bg-white rounded-lg">
                <p className="text-sm text-slate-600 mb-1">Improvement</p>
                <p className={`text-2xl font-bold ${efficiency.improvement >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {efficiency.improvement >= 0 ? '+' : ''}{efficiency.improvement?.toFixed(1)}
                </p>
              </div>
              <div className="text-center p-4 bg-white rounded-lg">
                <p className="text-sm text-slate-600 mb-1">Learning Rate</p>
                <p className="text-2xl font-bold text-blue-600">
                  {efficiency.learning_rate?.toFixed(3)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Memory System Stats */}
      <div className="grid md:grid-cols-3 gap-4">
        <Card className="border-purple-200 bg-gradient-to-br from-purple-50 to-white">
          <CardHeader>
            <CardTitle className="text-lg flex items-center space-x-2">
              <Database className="h-5 w-5 text-purple-600" />
              <span>Memory System</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Short-term:</span>
              <span className="font-semibold text-purple-600">{stats.short_term_count || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Mid-term:</span>
              <span className="font-semibold text-purple-600">{stats.mid_term_count || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Long-term patterns:</span>
              <span className="font-semibold text-purple-600">{stats.long_term_patterns || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Reflections:</span>
              <span className="font-semibold text-purple-600">{stats.reflective_insights || 0}</span>
            </div>
          </CardContent>
        </Card>

        <Card className="border-blue-200 bg-gradient-to-br from-blue-50 to-white">
          <CardHeader>
            <CardTitle className="text-lg flex items-center space-x-2">
              <BookOpen className="h-5 w-5 text-blue-600" />
              <span>Knowledge Base</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Successful patterns:</span>
              <span className="font-semibold text-blue-600">{knowledge.successful_patterns_count || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Failed patterns:</span>
              <span className="font-semibold text-blue-600">{knowledge.failed_patterns_count || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Success rate:</span>
              <span className="font-semibold text-blue-600">
                {((stats.success_rate || 0) * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Performance records:</span>
              <span className="font-semibold text-blue-600">{stats.performance_records || 0}</span>
            </div>
          </CardContent>
        </Card>

        <Card className="border-green-200 bg-gradient-to-br from-green-50 to-white">
          <CardHeader>
            <CardTitle className="text-lg flex items-center space-x-2">
              <Lightbulb className="h-5 w-5 text-green-600" />
              <span>Self-Improvement</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Cycles completed:</span>
              <span className="font-semibold text-green-600">
                {learningReport?.improvement_cycles_completed || 0}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Status:</span>
              <span className={`font-semibold ${efficiency.status === 'improving' ? 'text-green-600' : 'text-orange-600'}`}>
                {efficiency.status === 'improving' ? 'Improving' : efficiency.status || 'Active'}
              </span>
            </div>
            {knowledge.performance_trend && (
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-600">Trend:</span>
                <span className={`font-semibold ${knowledge.performance_trend.trend === 'improving' ? 'text-green-600' : 'text-orange-600'}`}>
                  {knowledge.performance_trend.trend}
                </span>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Recent Insights */}
      {knowledge.recent_insights && knowledge.recent_insights.length > 0 && (
        <Card className="border-indigo-200">
          <CardHeader>
            <CardTitle className="text-xl">🧠 Recent Reflective Insights</CardTitle>
            <CardDescription>Meta-learnings extracted from experiences</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {knowledge.recent_insights.map((insight, idx) => (
                <div key={idx} className="p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                  <div className="flex items-start space-x-3">
                    <div className="text-2xl">💡</div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-indigo-900">
                        {insight.content?.reflection?.meta_insight || 
                         insight.content?.type || 
                         'Reflective insight'}
                      </p>
                      {insight.content?.score && (
                        <p className="text-xs text-indigo-700 mt-1">
                          Score: {insight.content.score}/100
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Recommendations */}
      {learningReport?.recommendations && learningReport.recommendations.length > 0 && (
        <Card className="border-yellow-200 bg-yellow-50">
          <CardHeader>
            <CardTitle className="text-xl">📋 System Recommendations</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {learningReport.recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start space-x-2">
                  <span className="text-yellow-600 mt-0.5">▸</span>
                  <span className="text-slate-700 text-sm">{rec}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Performance Trend */}
      {knowledge.performance_trend && (
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">📈 Performance Trend Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="p-4 bg-slate-50 rounded-lg">
                <p className="text-sm text-slate-600 mb-1">Trend Direction</p>
                <p className={`text-xl font-bold ${knowledge.performance_trend.trend === 'improving' ? 'text-green-600' : 'text-orange-600'}`}>
                  {knowledge.performance_trend.trend === 'improving' ? '📈 Improving' : '📉 Declining'}
                </p>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg">
                <p className="text-sm text-slate-600 mb-1">Delta</p>
                <p className={`text-xl font-bold ${knowledge.performance_trend.delta >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {knowledge.performance_trend.delta >= 0 ? '+' : ''}{knowledge.performance_trend.delta?.toFixed(2)}
                </p>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg">
                <p className="text-sm text-slate-600 mb-1">Success Rate</p>
                <p className="text-xl font-bold text-blue-600">
                  {(knowledge.performance_trend.success_rate * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Info Box */}
      <Card className="border-slate-200 bg-slate-50">
        <CardContent className="pt-6">
          <div className="flex items-start space-x-3">
            <Brain className="h-6 w-6 text-indigo-600 mt-1" />
            <div>
              <p className="text-sm font-medium text-slate-800 mb-2">
                About Self-Learning System
              </p>
              <p className="text-xs text-slate-600 leading-relaxed">
                This system implements a <strong>Recursive Self-Improvement Loop</strong> using the 
                <strong> Reflexion framework</strong>. It features a hierarchical memory system 
                (short/mid/long-term), learns from execution results, applies the Ebbinghaus 
                forgetting curve, and conducts deep reflections to extract meta-learnings. 
                The agent continuously improves by analyzing its own performance trajectory.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SelfLearning;
