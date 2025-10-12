import { useState } from "react";
import "@/App.css";
import Generator from "./components/Generator";
import PatternLibrary from "./components/PatternLibrary";
import Dashboard from "./components/Dashboard";
import SelfLearning from "./components/SelfLearning";
import CopilotKitProvider from "./components/CopilotKitProvider";
import CopilotAssistant from "./components/CopilotAssistant";
import { Toaster } from "./components/ui/sonner";

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <CopilotKitProvider>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-sm border-b border-slate-200/50">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                CodeForge
              </h1>
              <p className="text-sm text-slate-600 mt-1.5 font-medium">
                Self-Improving AI Code Agent • Powered by Google Gemini 2.5
              </p>
            </div>
            <div className="flex items-center space-x-3">
              <div className="px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-full text-sm font-semibold shadow-lg">
                ⚡ Gemini 2.5
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white/60 backdrop-blur-sm border-b border-slate-200/50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex space-x-1">
            <button
              data-testid="nav-generate"
              onClick={() => setActiveTab('generate')}
              className={`py-4 px-6 font-semibold text-sm transition-all duration-200 relative ${
                activeTab === 'generate'
                  ? 'text-indigo-600'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <span className="relative z-10">🚀 Generate</span>
              {activeTab === 'generate' && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-indigo-600 to-purple-600"></div>
              )}
            </button>
            <button
              data-testid="nav-patterns"
              onClick={() => setActiveTab('patterns')}
              className={`py-4 px-6 font-semibold text-sm transition-all duration-200 relative ${
                activeTab === 'patterns'
                  ? 'text-indigo-600'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <span className="relative z-10">📚 Pattern Library</span>
              {activeTab === 'patterns' && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-indigo-600 to-purple-600"></div>
              )}
            </button>
            <button
              data-testid="nav-dashboard"
              onClick={() => setActiveTab('dashboard')}
              className={`py-4 px-6 font-semibold text-sm transition-all duration-200 relative ${
                activeTab === 'dashboard'
                  ? 'text-indigo-600'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <span className="relative z-10">📊 Dashboard</span>
              {activeTab === 'dashboard' && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-indigo-600 to-purple-600"></div>
              )}
            </button>
            <button
              data-testid="nav-self-learning"
              onClick={() => setActiveTab('self-learning')}
              className={`py-4 px-6 font-semibold text-sm transition-all duration-200 relative ${
                activeTab === 'self-learning'
                  ? 'text-indigo-600'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <span className="relative z-10">🧠 Self-Learning</span>
              {activeTab === 'self-learning' && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-indigo-600 to-purple-600"></div>
              )}
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === 'generate' && <Generator />}
        {activeTab === 'patterns' && <PatternLibrary />}
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'self-learning' && <SelfLearning />}
      </main>

      {/* Footer */}
      <footer className="bg-white/60 backdrop-blur-sm border-t border-slate-200/50 mt-16">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex justify-between text-sm text-slate-600 font-medium">
            <span>🏆 Built for AI Agents Hackathon 2025</span>
            <span>⚡ Multi-Agent A2A • Gemini 2.5 • CopilotKit</span>
          </div>
        </div>
      </footer>

      {/* CopilotKit AI Assistant */}
      <CopilotAssistant />

      {/* Toast Notifications */}
      <Toaster />
    </div>
    </CopilotKitProvider>
  );
}

export default App;