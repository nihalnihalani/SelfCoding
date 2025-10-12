import { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { ChevronDown, ChevronUp, TrendingUp, Star, Code } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PatternLibrary = () => {
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedPattern, setExpandedPattern] = useState(null);

  useEffect(() => {
    loadPatterns();
  }, []);

  const loadPatterns = async () => {
    try {
      const response = await axios.get(`${API}/patterns`);
      setPatterns(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load patterns:', error);
      toast.error('Failed to load patterns');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div data-testid="loading-patterns" className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading patterns...</p>
        </div>
      </div>
    );
  }

  if (patterns.length === 0) {
    return (
      <div data-testid="no-patterns" className="space-y-4">
        <div>
          <h2 className="text-3xl font-bold text-slate-800 mb-2">📚 Pattern Library</h2>
          <p className="text-slate-600">Learned patterns from successful generations</p>
        </div>
        <Card className="border-blue-200 bg-blue-50/50">
          <CardContent className="pt-6">
            <div className="text-center py-8">
              <div className="text-6xl mb-4">📚</div>
              <p className="text-blue-800 font-semibold text-lg">No patterns learned yet</p>
              <p className="text-blue-700 text-sm mt-2">Generate some apps to build the library!</p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6" data-testid="pattern-library-container">
      <div>
        <h2 className="text-3xl font-bold text-slate-800 mb-2">📚 Learned Pattern Library</h2>
        <p className="text-slate-600">Browse patterns the agent has learned from successful generations</p>
      </div>

      <div className="grid gap-4">
        {patterns.map((pattern) => (
          <Card
            key={pattern.id}
            data-testid={`pattern-card-${pattern.id}`}
            className="pattern-card border-slate-200 shadow-md hover:shadow-xl transition-all duration-200 overflow-hidden"
          >
            <button
              onClick={() => setExpandedPattern(
                expandedPattern === pattern.id ? null : pattern.id
              )}
              className="w-full text-left"
            >
              <CardHeader className="hover:bg-slate-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-xl text-slate-800 flex items-center space-x-2">
                      <span>✨</span>
                      <span>{pattern.description}</span>
                    </CardTitle>
                    <CardDescription className="mt-2 flex items-center space-x-4">
                      <span className="flex items-center space-x-1">
                        <TrendingUp className="w-4 h-4" />
                        <span>Used {pattern.usage_count} times</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <Star className="w-4 h-4 text-yellow-500" />
                        <span>Success rate: {(pattern.success_rate * 100).toFixed(0)}%</span>
                      </span>
                    </CardDescription>
                  </div>
                  <div className="text-slate-400">
                    {expandedPattern === pattern.id ? (
                      <ChevronUp className="w-6 h-6" />
                    ) : (
                      <ChevronDown className="w-6 h-6" />
                    )}
                  </div>
                </div>
              </CardHeader>
            </button>

            {expandedPattern === pattern.id && (
              <CardContent className="border-t border-slate-200 bg-slate-50">
                <div className="grid md:grid-cols-3 gap-6 mb-6">
                  <div className="text-center p-4 bg-white rounded-lg border border-slate-200">
                    <p className="text-sm font-medium text-slate-500 mb-1">Success Rate</p>
                    <p className="text-3xl font-bold text-green-600">
                      {(pattern.success_rate * 100).toFixed(0)}%
                    </p>
                  </div>
                  <div className="text-center p-4 bg-white rounded-lg border border-slate-200">
                    <p className="text-sm font-medium text-slate-500 mb-1">Times Used</p>
                    <p className="text-3xl font-bold text-blue-600">{pattern.usage_count}</p>
                  </div>
                  <div className="text-center p-4 bg-white rounded-lg border border-slate-200">
                    <p className="text-sm font-medium text-slate-500 mb-1">Technologies</p>
                    <p className="text-3xl font-bold text-purple-600">{pattern.tech_stack.length}</p>
                  </div>
                </div>

                {pattern.tech_stack.length > 0 && (
                  <div className="mb-4">
                    <p className="text-sm font-semibold text-slate-700 mb-3 flex items-center space-x-2">
                      <Code className="w-4 h-4" />
                      <span>Technologies:</span>
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {pattern.tech_stack.map((tech, index) => (
                        <Badge
                          key={index}
                          variant="secondary"
                          className="px-3 py-1 bg-blue-100 text-blue-700 border-blue-200"
                        >
                          {tech}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {pattern.features.length > 0 && (
                  <div className="mb-4">
                    <p className="text-sm font-semibold text-slate-700 mb-3">Features:</p>
                    <div className="flex flex-wrap gap-2">
                      {pattern.features.map((feature, index) => (
                        <Badge
                          key={index}
                          variant="secondary"
                          className="px-3 py-1 bg-green-100 text-green-700 border-green-200"
                        >
                          {feature}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                <div>
                  <p className="text-sm font-semibold text-slate-700 mb-3">Code Snippet:</p>
                  <div className="bg-slate-900 rounded-lg overflow-hidden">
                    <pre className="p-4 text-sm overflow-x-auto">
                      <code className="text-slate-100 font-mono">{pattern.code_snippet}</code>
                    </pre>
                  </div>
                </div>
              </CardContent>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
};

export default PatternLibrary;