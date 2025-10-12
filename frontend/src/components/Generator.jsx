import { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Switch } from './ui/switch';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';
import { toast } from 'sonner';
import CodeViewer from './CodeViewer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Generator = () => {
  const [description, setDescription] = useState('');
  const [useThinking, setUseThinking] = useState(true);
  const [autoTest, setAutoTest] = useState(false);
  const [maxIterations, setMaxIterations] = useState(2);
  
  const [generating, setGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusMessage, setStatusMessage] = useState('');
  const [result, setResult] = useState(null);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    // Connect to WebSocket
    const clientId = Math.random().toString(36).substring(7);
    const wsUrl = `${BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://')}/ws/${clientId}`;
    
    const websocket = new WebSocket(wsUrl);

    websocket.onopen = () => {
      console.log('WebSocket connected');
    };

    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setStatusMessage(message.message);
      if (message.progress !== undefined) {
        setProgress(message.progress);
      }
      if (message.type === 'complete') {
        setGenerating(false);
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    websocket.onclose = () => {
      console.log('WebSocket disconnected');
    };

    setWs(websocket);

    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  }, []);

  const handleGenerate = async () => {
    if (!description.trim()) {
      toast.error('Please describe your app first!');
      return;
    }

    setGenerating(true);
    setProgress(0);
    setResult(null);
    setStatusMessage('Starting generation...');

    try {
      const request = {
        description,
        use_thinking: useThinking,
        auto_test: autoTest,
        max_iterations: maxIterations,
      };

      const response = await axios.post(`${API}/generate`, request);
      setResult(response.data);
      setProgress(100);
      setStatusMessage('✅ Generation complete!');
      toast.success('App generated successfully!');
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.message;
      setStatusMessage(`❌ Error: ${errorMsg}`);
      setProgress(0);
      toast.error(`Generation failed: ${errorMsg}`);
    } finally {
      setGenerating(false);
    }
  };

  const handleFeedback = async (rating) => {
    if (!result || !result.files) return;

    const feedbackText = rating === 'failure' 
      ? prompt('What should improve?') 
      : null;

    try {
      await axios.post(`${API}/feedback`, {
        description,
        code: result.files,
        rating,
        feedback_text: feedbackText,
        metadata: result.metadata,
      });

      toast.success(
        rating === 'success' 
          ? '✅ Thanks! Learned from this success.' 
          : '📝 Noted! Will avoid this pattern.'
      );
    } catch (error) {
      console.error('Failed to submit feedback:', error);
      toast.error('Failed to submit feedback');
    }
  };

  return (
    <div className="space-y-6" data-testid="generator-container">
      <div>
        <h2 className="text-3xl font-bold text-slate-800 mb-2">🚀 Generate Your App</h2>
        <p className="text-slate-600">Describe what you want to build, and watch AI create it for you</p>
      </div>

      {/* Input Section */}
      <Card className="border-slate-200 shadow-lg bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-xl">App Description</CardTitle>
          <CardDescription>Be specific about features and functionality you want</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <Textarea
            data-testid="app-description-input"
            className="min-h-[120px] text-base border-slate-300 focus:border-indigo-500 focus:ring-indigo-500"
            placeholder="Example: Build me a todo app with dark mode, drag-and-drop reordering, categories, and local storage persistence. Make it visually stunning with smooth animations."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={generating}
          />

          {/* Options */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 border border-slate-200">
              <Label htmlFor="thinking-mode" className="text-sm font-medium cursor-pointer">
                🧠 Use Pro Planning
              </Label>
              <Switch
                id="thinking-mode"
                data-testid="thinking-mode-switch"
                checked={useThinking}
                onCheckedChange={setUseThinking}
                disabled={generating}
              />
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 border border-slate-200">
              <Label htmlFor="auto-test" className="text-sm font-medium cursor-pointer">
                🧪 Auto-test & Fix
              </Label>
              <Switch
                id="auto-test"
                data-testid="auto-test-switch"
                checked={autoTest}
                onCheckedChange={setAutoTest}
                disabled={generating}
              />
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 border border-slate-200">
              <Label htmlFor="max-iterations" className="text-sm font-medium">
                Max Fix Attempts
              </Label>
              <input
                id="max-iterations"
                data-testid="max-iterations-input"
                type="number"
                min="1"
                max="5"
                value={maxIterations}
                onChange={(e) => setMaxIterations(parseInt(e.target.value))}
                disabled={generating}
                className="w-16 px-3 py-1.5 text-center border border-slate-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Generate Button */}
          <Button
            data-testid="generate-button"
            onClick={handleGenerate}
            disabled={generating}
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white py-6 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
          >
            {generating ? '🤖 Generating...' : '🚀 Generate App'}
          </Button>
        </CardContent>
      </Card>

      {/* Progress Section */}
      {generating && (
        <Card data-testid="progress-card" className="border-indigo-200 bg-indigo-50/50 backdrop-blur-sm">
          <CardContent className="pt-6">
            <div className="mb-3 flex justify-between text-sm font-medium">
              <span className="text-indigo-700">{statusMessage}</span>
              <span className="text-indigo-600">{progress}%</span>
            </div>
            <Progress value={progress} className="h-3" />
          </CardContent>
        </Card>
      )}

      {/* Result Section */}
      {result && result.success && (
        <div className="space-y-6" data-testid="result-section">
          {/* Success Message */}
          <Card className="border-green-200 bg-green-50/50">
            <CardContent className="pt-6">
              <div className="flex items-start space-x-3">
                <div className="text-3xl">✅</div>
                <div className="flex-1">
                  <p className="text-green-800 font-semibold text-lg">App generated successfully!</p>
                  {result.patterns_used > 0 && (
                    <p className="text-green-700 text-sm mt-1">
                      ♻️ Reused {result.patterns_used} learned patterns! Generation was faster.
                    </p>
                  )}
                  <p className="text-green-700 text-sm">⏱️ Time taken: {result.time_taken.toFixed(2)}s</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Deployed URL */}
          {result.deployed_url && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center space-x-2">
                  <span>🌐</span>
                  <span>Deployed URL</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <a
                  data-testid="deployed-url-link"
                  href={result.deployed_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-indigo-600 hover:text-indigo-700 font-medium hover:underline break-all"
                >
                  {result.deployed_url}
                </a>
              </CardContent>
            </Card>
          )}

          {/* Code Viewer */}
          {result.files && <CodeViewer files={result.files} />}

          {/* Feedback Section */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">How was this generation?</CardTitle>
              <CardDescription>Your feedback helps the AI improve</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4">
                <Button
                  data-testid="feedback-success-button"
                  onClick={() => handleFeedback('success')}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white py-6 text-base font-semibold"
                >
                  👍 Perfect!
                </Button>
                <Button
                  data-testid="feedback-failure-button"
                  onClick={() => handleFeedback('failure')}
                  variant="destructive"
                  className="flex-1 py-6 text-base font-semibold"
                >
                  👎 Needs Work
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Error Section */}
      {result && !result.success && (
        <Card data-testid="error-card" className="border-red-200 bg-red-50/50">
          <CardContent className="pt-6">
            <div className="flex items-start space-x-3">
              <div className="text-3xl">❌</div>
              <div>
                <p className="text-red-800 font-semibold text-lg">Generation failed</p>
                <p className="text-red-700 text-sm mt-1">{result.error}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Generator;