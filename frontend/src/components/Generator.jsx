import { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Switch } from './ui/switch';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Progress, ProgressSteps } from './ui/progress';
import { toast } from '../lib/toast-config';
import CodeViewer from './CodeViewer';
import { 
  Sparkles, 
  Zap, 
  Info, 
  ChevronDown, 
  ChevronUp,
  Lightbulb,
  X
} from 'lucide-react';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from './ui/tooltip';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Template examples
const templates = [
  {
    id: 'todo',
    name: 'Todo App',
    description: 'Build me a todo app with dark mode, drag-and-drop reordering, categories, and local storage persistence. Make it visually stunning with smooth animations.',
    icon: '✅'
  },
  {
    id: 'dashboard',
    name: 'Analytics Dashboard',
    description: 'Create an analytics dashboard with interactive charts, data tables, filters, and real-time updates. Include multiple chart types like line, bar, and pie charts.',
    icon: '📊'
  },
  {
    id: 'landing',
    name: 'Landing Page',
    description: 'Design a modern landing page with hero section, features grid, testimonials, pricing table, and contact form. Make it responsive and visually appealing.',
    icon: '🚀'
  },
  {
    id: 'calculator',
    name: 'Calculator',
    description: 'Build a scientific calculator with basic operations, memory functions, and history. Include keyboard support and a clean, modern interface.',
    icon: '🔢'
  },
  {
    id: 'weather',
    name: 'Weather App',
    description: 'Create a weather app that shows current conditions, 5-day forecast, and location search. Include weather icons and temperature unit toggle.',
    icon: '🌤️'
  }
];

// Preset configurations
const presets = {
  quick: { useThinking: false, autoTest: false, maxIterations: 1 },
  balanced: { useThinking: true, autoTest: false, maxIterations: 2 },
  thorough: { useThinking: true, autoTest: true, maxIterations: 3 }
};

const Generator = () => {
  const [description, setDescription] = useState('');
  const [useThinking, setUseThinking] = useState(true);
  const [autoTest, setAutoTest] = useState(false);
  const [maxIterations, setMaxIterations] = useState(2);
  const [showTemplates, setShowTemplates] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [selectedPreset, setSelectedPreset] = useState('balanced');
  
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

      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev < 90) return prev + 10;
          return prev;
        });
      }, 1000);

      setStatusMessage('💻 Generating code with AI...');

      const response = await axios.post(`${API}/generate`, request, {
        timeout: 120000 // 2 minutes
      });
      
      clearInterval(progressInterval);
      
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

  const charCount = description.length;
  const charLimit = 1000;
  const charPercentage = (charCount / charLimit) * 100;

  const applyTemplate = (template) => {
    setDescription(template.description);
    setShowTemplates(false);
    toast.success(`Applied ${template.name} template`);
  };

  const applyPreset = (presetName) => {
    const preset = presets[presetName];
    setUseThinking(preset.useThinking);
    setAutoTest(preset.autoTest);
    setMaxIterations(preset.maxIterations);
    setSelectedPreset(presetName);
    toast.success(`Applied ${presetName} preset`);
  };

  const currentStep = generating 
    ? progress < 25 ? 0 
    : progress < 50 ? 1 
    : progress < 75 ? 2 
    : 3
    : -1;

  const generationSteps = [
    { label: 'Planning', description: 'Analyzing requirements' },
    { label: 'Generating', description: 'Creating code' },
    { label: 'Reviewing', description: 'Quality check' },
    { label: 'Complete', description: 'Finalizing' }
  ];

  return (
    <TooltipProvider>
      <div className="space-y-6" data-testid="generator-container">
        <div>
          <h2 className="text-3xl font-bold text-slate-800 dark:text-slate-200 mb-2">🚀 Generate Your App</h2>
          <p className="text-slate-600 dark:text-slate-400">Describe what you want to build, and watch AI create it for you</p>
        </div>

        {/* Input Section */}
        <Card className="border-slate-200 dark:border-slate-700 shadow-lg bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm transition-colors">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-xl">App Description</CardTitle>
                <CardDescription>Be specific about features and functionality you want</CardDescription>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowTemplates(!showTemplates)}
                className="flex items-center space-x-2"
              >
                <Lightbulb className="w-4 h-4" />
                <span>Templates</span>
                {showTemplates ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Template Selector */}
            <AnimatePresence>
              {showTemplates && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="overflow-hidden"
                >
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 pb-4">
                    {templates.map((template) => (
                      <button
                        key={template.id}
                        onClick={() => applyTemplate(template)}
                        disabled={generating}
                        className="p-4 text-left rounded-lg border border-slate-200 dark:border-slate-700 hover:border-indigo-500 dark:hover:border-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="text-2xl">{template.icon}</span>
                          <span className="font-semibold text-slate-800 dark:text-slate-200">{template.name}</span>
                        </div>
                        <p className="text-xs text-slate-600 dark:text-slate-400 line-clamp-2">
                          {template.description}
                        </p>
                      </button>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Textarea with character counter */}
            <div className="relative">
              <Textarea
                data-testid="app-description-input"
                className="min-h-[120px] text-base border-slate-300 dark:border-slate-600 focus:border-indigo-500 focus:ring-indigo-500 pr-20"
                placeholder="Example: Build me a todo app with dark mode, drag-and-drop reordering, categories, and local storage persistence. Make it visually stunning with smooth animations."
                value={description}
                onChange={(e) => {
                  if (e.target.value.length <= charLimit) {
                    setDescription(e.target.value);
                  }
                }}
                disabled={generating}
                maxLength={charLimit}
              />
              <div className="absolute bottom-3 right-3 flex items-center space-x-2">
                <div className={`text-xs font-medium ${
                  charPercentage > 90 
                    ? 'text-red-600 dark:text-red-400' 
                    : charPercentage > 75 
                    ? 'text-yellow-600 dark:text-yellow-400' 
                    : 'text-slate-500 dark:text-slate-400'
                }`}>
                  {charCount}/{charLimit}
                </div>
              </div>
            </div>

          {/* Preset Configurations */}
          <div className="flex items-center space-x-2 pb-2">
            <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Quick Presets:</span>
            <div className="flex space-x-2">
              {Object.keys(presets).map((presetName) => (
                <button
                  key={presetName}
                  onClick={() => applyPreset(presetName)}
                  disabled={generating}
                  className={`px-3 py-1 text-xs font-medium rounded-full transition-all duration-200 ${
                    selectedPreset === presetName
                      ? 'bg-indigo-600 text-white'
                      : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-300 dark:hover:bg-slate-600'
                  } disabled:opacity-50 disabled:cursor-not-allowed capitalize`}
                >
                  {presetName}
                </button>
              ))}
            </div>
          </div>

          {/* Advanced Options Toggle */}
          <button
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center space-x-2 text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors"
          >
            <span>{showAdvanced ? 'Hide' : 'Show'} Advanced Options</span>
            {showAdvanced ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {/* Options */}
          <AnimatePresence>
            {showAdvanced && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="overflow-hidden"
              >
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                    <div className="flex items-center space-x-2">
                      <Label htmlFor="thinking-mode" className="text-sm font-medium cursor-pointer">
                        🧠 Use Pro Planning
                      </Label>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Info className="w-4 h-4 text-slate-400 cursor-help" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p className="max-w-xs">Uses Gemini 2.5 Pro for better planning and architecture</p>
                        </TooltipContent>
                      </Tooltip>
                    </div>
                    <Switch
                      id="thinking-mode"
                      data-testid="thinking-mode-switch"
                      checked={useThinking}
                      onCheckedChange={(checked) => {
                        setUseThinking(checked);
                        setSelectedPreset('custom');
                      }}
                      disabled={generating}
                    />
                  </div>

                  <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                    <div className="flex items-center space-x-2">
                      <Label htmlFor="auto-test" className="text-sm font-medium cursor-pointer">
                        🧪 Auto-test & Fix
                      </Label>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Info className="w-4 h-4 text-slate-400 cursor-help" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p className="max-w-xs">Automatically tests and fixes code issues</p>
                        </TooltipContent>
                      </Tooltip>
                    </div>
                    <Switch
                      id="auto-test"
                      data-testid="auto-test-switch"
                      checked={autoTest}
                      onCheckedChange={(checked) => {
                        setAutoTest(checked);
                        setSelectedPreset('custom');
                      }}
                      disabled={generating}
                    />
                  </div>

                  <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                    <div className="flex items-center space-x-2">
                      <Label htmlFor="max-iterations" className="text-sm font-medium">
                        Max Fix Attempts
                      </Label>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Info className="w-4 h-4 text-slate-400 cursor-help" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p className="max-w-xs">Number of times to retry if generation fails</p>
                        </TooltipContent>
                      </Tooltip>
                    </div>
                    <input
                      id="max-iterations"
                      data-testid="max-iterations-input"
                      type="number"
                      min="1"
                      max="5"
                      value={maxIterations}
                      onChange={(e) => {
                        setMaxIterations(parseInt(e.target.value));
                        setSelectedPreset('custom');
                      }}
                      disabled={generating}
                      className="w-16 px-3 py-1.5 text-center border border-slate-300 dark:border-slate-600 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-slate-900"
                    />
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

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
      <AnimatePresence>
        {generating && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Card data-testid="progress-card" className="border-indigo-200 dark:border-indigo-800 bg-indigo-50/50 dark:bg-indigo-900/20 backdrop-blur-sm">
              <CardContent className="pt-6 space-y-6">
                {/* Multi-step Progress Indicator */}
                <ProgressSteps 
                  steps={generationSteps} 
                  currentStep={currentStep}
                />
                
                {/* Status Message */}
                <div className="text-center">
                  <motion.div
                    key={statusMessage}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center justify-center space-x-2 text-indigo-700 dark:text-indigo-300 font-medium"
                  >
                    <Sparkles className="w-5 h-5 animate-pulse" />
                    <span>{statusMessage}</span>
                  </motion.div>
                </div>

                {/* Progress Bar */}
                <div>
                  <Progress 
                    value={progress} 
                    gradient={true}
                    showPercentage={true}
                    size="lg"
                  />
                </div>

                {/* Cancel Button */}
                <div className="flex justify-center">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      setGenerating(false);
                      setProgress(0);
                      toast.info('Generation cancelled');
                    }}
                    className="text-slate-600 dark:text-slate-400"
                  >
                    <X className="w-4 h-4 mr-2" />
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Result Section */}
      <AnimatePresence>
        {result && result.success && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.4 }}
            className="space-y-6" 
            data-testid="result-section"
          >
            {/* Success Message */}
            <Card className="border-green-200 dark:border-green-800 bg-green-50/50 dark:bg-green-900/20 overflow-hidden">
              <motion.div
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="h-1 bg-gradient-to-r from-green-500 to-emerald-500"
              />
              <CardContent className="pt-6">
                <div className="flex items-start space-x-3">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 200, delay: 0.3 }}
                    className="text-3xl"
                  >
                    ✅
                  </motion.div>
                  <div className="flex-1">
                    <p className="text-green-800 dark:text-green-200 font-semibold text-lg">App generated successfully!</p>
                    {result.patterns_used > 0 && (
                      <p className="text-green-700 dark:text-green-300 text-sm mt-1">
                        ♻️ Reused {result.patterns_used} learned patterns! Generation was faster.
                      </p>
                    )}
                    <p className="text-green-700 dark:text-green-300 text-sm">⏱️ Time taken: {result.time_taken.toFixed(2)}s</p>
                  
                  {/* A2A Multi-Agent Info */}
                  {result.metadata?.orchestrated_by && (
                    <div className="mt-3 pt-3 border-t border-green-200">
                      <p className="text-green-800 font-medium text-sm mb-2">🤖 Multi-Agent Workflow:</p>
                      <div className="space-y-1">
                        {result.metadata?.workflow_log?.map((log, idx) => (
                          <p key={idx} className="text-green-700 text-xs">
                            • {log.step}: {log.status} {log.quality_score && `(Score: ${log.quality_score})`}
                          </p>
                        ))}
                      </div>
                      {result.metadata?.code_review && (
                        <div className="mt-2 p-2 bg-green-100 rounded">
                          <p className="text-green-800 text-xs font-medium">
                            📋 Code Review: Quality Score {result.metadata.code_review.quality_score}/100
                            {result.metadata.code_review.approved ? " ✓ Approved" : " ⚠ Needs Attention"}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
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
          <Card className="border-slate-200 dark:border-slate-700">
            <CardHeader>
              <CardTitle className="text-lg">How was this generation?</CardTitle>
              <CardDescription>Your feedback helps the AI improve</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4">
                <motion.div className="flex-1" whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Button
                    data-testid="feedback-success-button"
                    onClick={() => handleFeedback('success')}
                    className="w-full bg-green-600 hover:bg-green-700 text-white py-6 text-base font-semibold shadow-lg hover:shadow-xl transition-all"
                  >
                    👍 Perfect!
                  </Button>
                </motion.div>
                <motion.div className="flex-1" whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Button
                    data-testid="feedback-failure-button"
                    onClick={() => handleFeedback('failure')}
                    variant="destructive"
                    className="w-full py-6 text-base font-semibold shadow-lg hover:shadow-xl transition-all"
                  >
                    👎 Needs Work
                  </Button>
                </motion.div>
              </div>
            </CardContent>
          </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error Section */}
      <AnimatePresence>
        {result && !result.success && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.4 }}
          >
            <Card data-testid="error-card" className="border-red-200 dark:border-red-800 bg-red-50/50 dark:bg-red-900/20 overflow-hidden">
              <motion.div
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="h-1 bg-gradient-to-r from-red-500 to-rose-500"
              />
              <CardContent className="pt-6">
                <div className="flex items-start space-x-3">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 200, delay: 0.3 }}
                    className="text-3xl"
                  >
                    ❌
                  </motion.div>
                  <div className="flex-1">
                    <p className="text-red-800 dark:text-red-200 font-semibold text-lg">Generation failed</p>
                    <p className="text-red-700 dark:text-red-300 text-sm mt-1">{result.error}</p>
                    <div className="mt-4">
                      <Button
                        onClick={() => {
                          setResult(null);
                          handleGenerate();
                        }}
                        variant="outline"
                        className="border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 hover:bg-red-100 dark:hover:bg-red-900/30"
                      >
                        <Zap className="w-4 h-4 mr-2" />
                        Try Again
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
      </div>
    </TooltipProvider>
  );
};

export default Generator;