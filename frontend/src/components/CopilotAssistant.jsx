import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotAction, useCopilotReadable } from "@copilotkit/react-core";
import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Bot, X, Sparkles } from "lucide-react";
import axios from "axios";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CopilotAssistant = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [generatedApps, setGeneratedApps] = useState([]);
  const [systemStats, setSystemStats] = useState(null);

  // Load system stats
  useEffect(() => {
    const loadStats = async () => {
      try {
        const [metricsRes, patternsRes] = await Promise.all([
          axios.get(`${API}/metrics`),
          axios.get(`${API}/patterns`)
        ]);
        setSystemStats({
          metrics: metricsRes.data,
          patterns: patternsRes.data
        });
      } catch (error) {
        console.error('Failed to load stats:', error);
      }
    };
    loadStats();
  }, []);

  // Make system stats readable to Copilot
  useCopilotReadable({
    description: "CodeForge system statistics and performance metrics",
    value: systemStats,
  });

  // Make app generation history readable to Copilot
  useCopilotReadable({
    description: "History of generated applications",
    value: generatedApps,
  });

  // Action 1: Generate App
  useCopilotAction({
    name: "generate_app",
    description: "Generate a complete web application with HTML, CSS, and JavaScript",
    parameters: [
      {
        name: "description",
        type: "string",
        description: "Detailed description of the app to generate",
        required: true,
      },
    ],
    handler: async ({ description }) => {
      try {
        toast.info("Starting app generation...");
        
        const response = await axios.post(`${API}/generate`, {
          description,
          use_thinking: true,
          auto_test: false,
          max_iterations: 1
        }, { timeout: 60000 });
        
        if (response.data.success) {
          setGeneratedApps(prev => [...prev, { 
            description, 
            timestamp: new Date(),
            files: Object.keys(response.data.files || {})
          }]);
          
          toast.success("App generated successfully!");
          
          return `✅ Successfully generated app!\n\nFiles created: ${Object.keys(response.data.files || {}).join(', ')}\n\nTime taken: ${response.data.time_taken?.toFixed(1)}s\n\nYou can view the code in the Generate tab!`;
        } else {
          return `❌ Generation failed: ${response.data.error}`;
        }
      } catch (error) {
        const errorMsg = error.response?.data?.detail || error.message;
        toast.error(`Generation failed: ${errorMsg}`);
        return `❌ Error generating app: ${errorMsg}`;
      }
    },
  });

  // Action 2: Get Pattern Library Stats
  useCopilotAction({
    name: "check_patterns",
    description: "Check the pattern library and learned patterns",
    parameters: [],
    handler: async () => {
      try {
        const response = await axios.get(`${API}/patterns`);
        const patterns = response.data;
        
        if (patterns.length === 0) {
          return "📚 No patterns learned yet. Generate some apps to build the library!";
        }
        
        return `📚 Pattern Library:\n\n${patterns.length} patterns learned!\n\nTop patterns:\n${patterns.slice(0, 3).map((p, i) => 
          `${i + 1}. ${p.description} (used ${p.usage_count} times)`
        ).join('\n')}\n\nView all patterns in the Pattern Library tab!`;
      } catch (error) {
        return `Error fetching patterns: ${error.message}`;
      }
    },
  });

  // Action 3: Get Dashboard Metrics
  useCopilotAction({
    name: "show_metrics",
    description: "Show performance metrics and dashboard statistics",
    parameters: [],
    handler: async () => {
      try {
        const response = await axios.get(`${API}/metrics`);
        const metrics = response.data;
        
        return `📊 CodeForge Metrics:\n\n✓ Total Apps: ${metrics.total_apps}\n✓ Successful: ${metrics.successful_apps}\n✓ Success Rate: ${(metrics.success_rate * 100).toFixed(1)}%\n✓ Patterns Learned: ${metrics.pattern_count}\n✓ Failed Attempts: ${metrics.failed_attempts}\n\nView detailed charts in the Dashboard tab!`;
      } catch (error) {
        return `Error fetching metrics: ${error.message}`;
      }
    },
  });

  // Action 4: Get Self-Learning Report
  useCopilotAction({
    name: "check_learning",
    description: "Check self-learning system status and learning efficiency",
    parameters: [],
    handler: async () => {
      try {
        const response = await axios.get(`${API}/self-learning/report`);
        const report = response.data;
        
        const efficiency = report.learning_efficiency || {};
        
        let result = `🧠 Self-Learning System:\n\n`;
        result += `Improvement Cycles: ${report.improvement_cycles_completed}\n`;
        
        if (efficiency.status !== 'insufficient_data') {
          result += `\nLearning Efficiency:\n`;
          result += `• Status: ${efficiency.status}\n`;
          result += `• Early Avg: ${efficiency.early_average?.toFixed(1)}\n`;
          result += `• Recent Avg: ${efficiency.recent_average?.toFixed(1)}\n`;
          result += `• Improvement: ${efficiency.improvement >= 0 ? '+' : ''}${efficiency.improvement?.toFixed(1)}\n`;
        }
        
        if (report.recommendations && report.recommendations.length > 0) {
          result += `\nRecommendations:\n${report.recommendations.slice(0, 3).map(r => `• ${r}`).join('\n')}`;
        }
        
        result += `\n\nView detailed analytics in the Self-Learning tab!`;
        
        return result;
      } catch (error) {
        return `Error fetching learning report: ${error.message}`;
      }
    },
  });

  useEffect(() => {
    // Auto-open on first visit
    const hasVisited = localStorage.getItem('copilot_visited');
    if (!hasVisited) {
      setTimeout(() => {
        setIsOpen(true);
        localStorage.setItem('copilot_visited', 'true');
      }, 2000);
    }
  }, []);

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <Button
          data-testid="copilot-open-button"
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 h-14 w-14 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-xl hover:shadow-2xl transition-all duration-200 z-50"
        >
          <Bot className="h-6 w-6 text-white" />
        </Button>
      )}

      {/* Chat Panel */}
      {isOpen && (
        <div 
          data-testid="copilot-chat-panel"
          className="fixed bottom-6 right-6 w-96 h-[600px] bg-white rounded-2xl shadow-2xl overflow-hidden z-50 flex flex-col border-2 border-indigo-200"
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Bot className="h-6 w-6 text-white" />
              <div>
                <h3 className="text-white font-semibold">AI Assistant</h3>
                <p className="text-indigo-100 text-xs">Powered by A2A Multi-Agent System</p>
              </div>
            </div>
            <Button
              data-testid="copilot-close-button"
              onClick={() => setIsOpen(false)}
              variant="ghost"
              size="sm"
              className="text-white hover:bg-indigo-700"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Chat Content */}
          <div className="flex-1 overflow-hidden">
            <CopilotChat
              labels={{
                title: "CodeForge Assistant",
                initial: "Hi! I'm your AI coding assistant. I can help you generate web applications using our multi-agent system. Just describe what you want to build!",
              }}
            />
          </div>

          {/* Footer */}
          <div className="p-3 bg-slate-50 border-t border-slate-200">
            <p className="text-xs text-center text-slate-600">
              🤖 Multi-Agent • A2A Protocol • Gemini 2.5
            </p>
          </div>
        </div>
      )}
    </>
  );
};

export default CopilotAssistant;
