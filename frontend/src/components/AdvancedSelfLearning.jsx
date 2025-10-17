import { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Brain, TrendingUp, Database, Lightbulb, RefreshCw, BookOpen, 
  Target, Award, Clock, BarChart3, Zap, AlertCircle, 
  GraduationCap, Compass, Layers, Activity 
} from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdvancedSelfLearning = () => {
  const [comprehensiveReport, setComprehensiveReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeInsight, setActiveInsight] = useState(null);

  useEffect(() => {
    loadComprehensiveData();
    const interval = setInterval(loadComprehensiveData, 15000);
    return () => clearInterval(interval);
  }, []);

  const loadComprehensiveData = async () => {
    try {
      // This would call the new comprehensive learning report endpoint
      const response = await axios.get(`${API}/self-learning/comprehensive-report`);
      setComprehensiveReport(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load comprehensive learning data:', error);
      // Fallback to mock data for demonstration
      setComprehensiveReport(generateMockData());
      setLoading(false);
    }
  };

  const generateMockData = () => ({
    overall_learning_score: 73.5,
    score_breakdown: [
      "Curriculum Mastery: 22.5/30",
      "Memory Performance: 18.7/25", 
      "Reflection Quality: 16.8/20",
      "Learning Velocity: 15.5/25"
    ],
    improvement_cycles_completed: 47,
    curriculum_progress: {
      total_tasks_attempted: 12,
      mastered_tasks: 8,
      mastery_rate: 0.67,
      current_difficulty_level: "INTERMEDIATE",
      focus_areas: ["data_visualization", "interactive_apps"],
      learning_velocity_per_week: 2.3,
      next_recommended_tasks: [
        {
          id: "chart_dashboard",
          description: "Build a dashboard with interactive charts",
          difficulty: "ADVANCED",
          estimated_time: 30
        },
        {
          id: "real_time_chat", 
          description: "Create a real-time chat application",
          difficulty: "ADVANCED",
          estimated_time: 45
        }
      ]
    },
    meta_learning_insights: {
      strategy_performance: {
        imitation: { success_rate: 0.85, avg_quality: 78.2, usage_count: 15 },
        exploration: { success_rate: 0.62, avg_quality: 71.5, usage_count: 8 },
        refinement: { success_rate: 0.91, avg_quality: 82.1, usage_count: 12 },
        transfer: { success_rate: 0.73, avg_quality: 75.8, usage_count: 6 },
        composition: { success_rate: 0.68, avg_quality: 79.3, usage_count: 4 }
      },
      learning_trajectory: {
        recent_avg_quality: 79.4,
        early_avg_quality: 65.2,
        improvement: 14.2
      },
      domain_mastery: {
        ui_components: { success_rate: 0.89, avg_quality: 81.5, mastery_level: "proficient" },
        data_visualization: { success_rate: 0.71, avg_quality: 74.2, mastery_level: "learning" },
        interactive_apps: { success_rate: 0.65, avg_quality: 72.8, mastery_level: "learning" }
      }
    },
    reflection_summary: {
      total_reflections: 34,
      insights_by_type: {
        performance: 12,
        error_analysis: 8,
        pattern_discovery: 9,
        strategy_optimization: 5
      },
      average_confidence: 0.78,
      average_impact: 0.72,
      recent_confidence_trend: 0.82,
      most_recent_insights: [
        {
          type: "pattern_discovery",
          content: "Quality improving: 71.2 → 79.4. Learning is effective.",
          confidence: 0.85,
          impact: 0.8
        },
        {
          type: "strategy_optimization", 
          content: "Refinement strategy showing highest success rate (91%)",
          confidence: 0.9,
          impact: 0.85
        }
      ]
    },
    learning_efficiency: {
      total_learning_time_minutes: 420,
      learning_velocity_per_hour: 2.1,
      time_efficiency: 0.74,
      strategy_efficiency: {
        imitation: 1.2,
        exploration: 0.8,
        refinement: 1.5,
        transfer: 1.0,
        composition: 0.9
      }
    },
    recommendations: [
      "Continue using refinement strategy - showing highest success rate",
      "Focus on data visualization domain to improve mastery",
      "Increase reflection depth for better insights"
    ],
    next_suggested_task: "Build an interactive data dashboard with real-time updates",
    learning_trajectory: "improving"
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading advanced learning analytics...</p>
        </div>
      </div>
    );
  }

  const report = comprehensiveReport;

  return (
    <div className="space-y-6">
      {/* Header with Overall Score */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-800 mb-2 flex items-center space-x-3">
            <Brain className="h-8 w-8 text-indigo-600" />
            <span>Advanced Self-Learning</span>
          </h2>
          <p className="text-slate-600">Research-backed multi-agent learning system</p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold text-indigo-600">
            {(report?.overall_learning_score ?? 0).toFixed(1)}
          </div>
          <div className="text-sm text-slate-600">Learning Score</div>
          <Badge variant={report?.learning_trajectory === 'improving' ? 'default' : 'secondary'}>
            {report?.learning_trajectory || 'developing'}
          </Badge>
        </div>
      </div>

      {/* Score Breakdown */}
      <Card className="border-indigo-200 bg-gradient-to-r from-indigo-50 to-purple-50">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <BarChart3 className="h-5 w-5" />
            <span>Learning Score Breakdown</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {(report?.score_breakdown || []).map((item, idx) => {
              const [label, score] = item.split(': ');
              const [current, max] = score.split('/');
              const percentage = (parseFloat(current) / parseFloat(max)) * 100;
              
              return (
                <div key={idx} className="text-center">
                  <div className="text-sm text-slate-600 mb-2">{label}</div>
                  <Progress value={percentage} className="h-2 mb-2" />
                  <div className="text-lg font-bold text-slate-800">{score}</div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Main Tabs */}
      <Tabs defaultValue="curriculum" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="curriculum" className="flex items-center space-x-2">
            <GraduationCap className="h-4 w-4" />
            <span>Curriculum</span>
          </TabsTrigger>
          <TabsTrigger value="meta-learning" className="flex items-center space-x-2">
            <Compass className="h-4 w-4" />
            <span>Meta-Learning</span>
          </TabsTrigger>
          <TabsTrigger value="reflection" className="flex items-center space-x-2">
            <Lightbulb className="h-4 w-4" />
            <span>Reflection</span>
          </TabsTrigger>
          <TabsTrigger value="efficiency" className="flex items-center space-x-2">
            <Zap className="h-4 w-4" />
            <span>Efficiency</span>
          </TabsTrigger>
        </TabsList>

        {/* Curriculum Learning Tab */}
        <TabsContent value="curriculum" className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Target className="h-5 w-5 text-green-600" />
                  <span>Mastery Progress</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Tasks Mastered</span>
                      <span>{report?.curriculum_progress?.mastered_tasks || 0}/{report?.curriculum_progress?.total_tasks_attempted || 0}</span>
                    </div>
                    <Progress value={(report?.curriculum_progress?.mastery_rate || 0) * 100} className="h-3" />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div className="p-3 bg-blue-50 rounded-lg">
                      <div className="text-lg font-bold text-blue-600">
                        {report?.curriculum_progress?.current_difficulty_level || 'BEGINNER'}
                      </div>
                      <div className="text-xs text-blue-700">Current Level</div>
                    </div>
                    <div className="p-3 bg-green-50 rounded-lg">
                      <div className="text-lg font-bold text-green-600">
                        {(report?.curriculum_progress?.learning_velocity_per_week || 0).toFixed(1)}
                      </div>
                      <div className="text-xs text-green-700">Tasks/Week</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BookOpen className="h-5 w-5 text-purple-600" />
                  <span>Focus Areas</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {(report?.curriculum_progress?.focus_areas || []).map((area, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2 bg-purple-50 rounded">
                      <span className="text-sm font-medium text-purple-800">
                        {area.replace('_', ' ').toUpperCase()}
                      </span>
                      <Badge variant="secondary">Focus</Badge>
                    </div>
                  ))}
                  {(!report?.curriculum_progress?.focus_areas || report.curriculum_progress.focus_areas.length === 0) && (
                    <p className="text-sm text-slate-500">No focus areas identified yet</p>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Next Recommended Tasks */}
          <Card>
            <CardHeader>
              <CardTitle>📋 Next Recommended Tasks</CardTitle>
              <CardDescription>Curriculum-guided task suggestions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {(report?.curriculum_progress?.next_recommended_tasks || []).map((task, idx) => (
                  <div key={idx} className="flex items-center justify-between p-4 border rounded-lg hover:bg-slate-50">
                    <div className="flex-1">
                      <div className="font-medium text-slate-800">{task.description}</div>
                      <div className="text-sm text-slate-600 mt-1">
                        Difficulty: {task.difficulty} • Est. {task.estimated_time} min
                      </div>
                    </div>
                    <Button size="sm" variant="outline">
                      Try Task
                    </Button>
                  </div>
                ))}
                {(!report?.curriculum_progress?.next_recommended_tasks || report.curriculum_progress.next_recommended_tasks.length === 0) && (
                  <p className="text-sm text-slate-500">No task recommendations available yet</p>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Meta-Learning Tab */}
        <TabsContent value="meta-learning" className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>🎯 Strategy Performance</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {Object.entries(report?.meta_learning_insights?.strategy_performance || {}).map(([strategy, perf]) => (
                    <div key={strategy} className="flex items-center justify-between p-3 border rounded">
                      <div>
                        <div className="font-medium capitalize">{strategy}</div>
                        <div className="text-sm text-slate-600">
                          {perf?.usage_count || 0} uses • {(perf?.avg_quality || 0).toFixed(1)} avg quality
                        </div>
                      </div>
                      <div className="text-right">
                        <div className={`font-bold ${(perf?.success_rate || 0) > 0.8 ? 'text-green-600' : (perf?.success_rate || 0) > 0.6 ? 'text-yellow-600' : 'text-red-600'}`}>
                          {((perf?.success_rate || 0) * 100).toFixed(0)}%
                        </div>
                        <div className="text-xs text-slate-500">Success</div>
                      </div>
                    </div>
                  ))}
                  {Object.keys(report?.meta_learning_insights?.strategy_performance || {}).length === 0 && (
                    <p className="text-sm text-slate-500">No strategy data available yet</p>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>🏆 Domain Mastery</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {Object.entries(report?.meta_learning_insights?.domain_mastery || {}).map(([domain, mastery]) => (
                    <div key={domain} className="p-3 border rounded">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium capitalize">{domain.replace('_', ' ')}</span>
                        <Badge variant={
                          mastery?.mastery_level === 'expert' ? 'default' :
                          mastery?.mastery_level === 'proficient' ? 'secondary' : 'outline'
                        }>
                          {mastery?.mastery_level || 'learning'}
                        </Badge>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div>Success: {((mastery?.success_rate || 0) * 100).toFixed(0)}%</div>
                        <div>Quality: {(mastery?.avg_quality || 0).toFixed(1)}</div>
                      </div>
                    </div>
                  ))}
                  {Object.keys(report?.meta_learning_insights?.domain_mastery || {}).length === 0 && (
                    <p className="text-sm text-slate-500">No domain mastery data yet</p>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Learning Trajectory */}
          <Card>
            <CardHeader>
              <CardTitle>📈 Learning Trajectory</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4 text-center">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">
                    {(report?.meta_learning_insights?.learning_trajectory?.early_avg_quality || 0).toFixed(1)}
                  </div>
                  <div className="text-sm text-blue-700">Early Average</div>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">
                    {(report?.meta_learning_insights?.learning_trajectory?.recent_avg_quality || 0).toFixed(1)}
                  </div>
                  <div className="text-sm text-green-700">Recent Average</div>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">
                    +{(report?.meta_learning_insights?.learning_trajectory?.improvement || 0).toFixed(1)}
                  </div>
                  <div className="text-sm text-purple-700">Improvement</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Reflection Tab */}
        <TabsContent value="reflection" className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Layers className="h-5 w-5" />
                  <span>Reflection Analytics</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div className="p-3 bg-indigo-50 rounded-lg">
                      <div className="text-lg font-bold text-indigo-600">
                        {report?.reflection_summary?.total_reflections || 0}
                      </div>
                      <div className="text-xs text-indigo-700">Total Reflections</div>
                    </div>
                    <div className="p-3 bg-green-50 rounded-lg">
                      <div className="text-lg font-bold text-green-600">
                        {((report?.reflection_summary?.average_confidence || 0) * 100).toFixed(0)}%
                      </div>
                      <div className="text-xs text-green-700">Avg Confidence</div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="text-sm font-medium mb-2">Reflection Types</div>
                    <div className="space-y-2">
                      {Object.entries(report?.reflection_summary?.insights_by_type || {}).map(([type, count]) => (
                        <div key={type} className="flex justify-between text-sm">
                          <span className="capitalize">{type.replace('_', ' ')}</span>
                          <span className="font-medium">{count}</span>
                        </div>
                      ))}
                      {Object.keys(report?.reflection_summary?.insights_by_type || {}).length === 0 && (
                        <p className="text-sm text-slate-500">No reflection data yet</p>
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>💡 Recent Insights</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {(report?.reflection_summary?.most_recent_insights || []).map((insight, idx) => (
                    <div key={idx} className="p-3 border rounded-lg">
                      <div className="flex items-start justify-between mb-2">
                        <Badge variant="outline" className="text-xs">
                          {insight?.type?.replace('_', ' ') || 'insight'}
                        </Badge>
                        <div className="text-xs text-slate-500">
                          {((insight?.confidence || 0) * 100).toFixed(0)}% confidence
                        </div>
                      </div>
                      <p className="text-sm text-slate-700">{insight?.content || 'No content'}</p>
                      <div className="mt-2">
                        <Progress value={(insight?.impact || 0) * 100} className="h-1" />
                        <div className="text-xs text-slate-500 mt-1">
                          Impact: {((insight?.impact || 0) * 100).toFixed(0)}%
                        </div>
                      </div>
                    </div>
                  ))}
                  {(!report?.reflection_summary?.most_recent_insights || report.reflection_summary.most_recent_insights.length === 0) && (
                    <p className="text-sm text-slate-500">No recent insights available</p>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Efficiency Tab */}
        <TabsContent value="efficiency" className="space-y-4">
          <div className="grid md:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Clock className="h-5 w-5 text-blue-600" />
                  <span>Time Efficiency</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">
                    {((report?.learning_efficiency?.time_efficiency || 0) * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-slate-600 mt-1">
                    {report?.learning_efficiency?.total_learning_time_minutes || 0} min total
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Activity className="h-5 w-5 text-green-600" />
                  <span>Learning Velocity</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">
                    {(report?.learning_efficiency?.learning_velocity_per_hour || 0).toFixed(1)}
                  </div>
                  <div className="text-sm text-slate-600 mt-1">
                    Quality points/hour
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Award className="h-5 w-5 text-purple-600" />
                  <span>Best Strategy</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  {(() => {
                    const strategies = Object.entries(report?.learning_efficiency?.strategy_efficiency || {});
                    if (strategies.length === 0) {
                      return <div className="text-sm text-slate-500">No data yet</div>;
                    }
                    const bestStrategy = strategies.reduce((a, b) => a[1] > b[1] ? a : b);
                    return (
                      <>
                        <div className="text-lg font-bold text-purple-600 capitalize">
                          {bestStrategy[0]}
                        </div>
                        <div className="text-sm text-slate-600 mt-1">
                          {bestStrategy[1].toFixed(1)} efficiency
                        </div>
                      </>
                    );
                  })()}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Strategy Efficiency Chart */}
          <Card>
            <CardHeader>
              <CardTitle>⚡ Strategy Efficiency Comparison</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(report?.learning_efficiency?.strategy_efficiency || {}).map(([strategy, efficiency]) => (
                  <div key={strategy} className="flex items-center space-x-3">
                    <div className="w-20 text-sm capitalize">{strategy}</div>
                    <div className="flex-1">
                      <Progress value={(efficiency / 2) * 100} className="h-3" />
                    </div>
                    <div className="w-12 text-sm font-medium">{efficiency.toFixed(1)}</div>
                  </div>
                ))}
                {Object.keys(report?.learning_efficiency?.strategy_efficiency || {}).length === 0 && (
                  <p className="text-sm text-slate-500">No strategy efficiency data yet</p>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Recommendations */}
      <Card className="border-yellow-200 bg-yellow-50">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <AlertCircle className="h-5 w-5 text-yellow-600" />
            <span>AI Recommendations</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {(report?.recommendations || []).map((rec, idx) => (
              <div key={idx} className="flex items-start space-x-2">
                <span className="text-yellow-600 mt-0.5">▸</span>
                <span className="text-slate-700 text-sm">{rec}</span>
              </div>
            ))}
            {(!report?.recommendations || report.recommendations.length === 0) && (
              <p className="text-sm text-slate-500">No recommendations at this time</p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Next Suggested Task */}
      {report?.next_suggested_task && (
        <Card className="border-indigo-200 bg-indigo-50">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="h-5 w-5 text-indigo-600" />
              <span>Next Suggested Task</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <p className="text-slate-700">{report.next_suggested_task}</p>
              <Button className="bg-indigo-600 hover:bg-indigo-700">
                Start Task
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default AdvancedSelfLearning;