import { useState } from "react";
import "@/App.css";
import Generator from "./components/Generator";
import PatternLibrary from "./components/PatternLibrary";
import Dashboard from "./components/Dashboard";
import SelfLearning from "./components/SelfLearning";
import AdvancedSelfLearning from "./components/AdvancedSelfLearning";
import CopilotKitProvider from "./components/CopilotKitProvider";
import CopilotAssistant from "./components/CopilotAssistant";
import { Toaster } from "./components/ui/sonner";
import { ThemeProvider } from "./contexts/ThemeContext";
import ThemeToggle from "./components/ThemeToggle";
import { toasterConfig } from "./lib/toast-config";
import Navigation from "./components/Navigation";

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <ThemeProvider defaultTheme="system">
      <CopilotKitProvider>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 transition-colors duration-300">
        {/* Header */}
        <header className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md shadow-sm border-b border-slate-200/50 dark:border-slate-700/50 transition-colors duration-300">
          <div className="max-w-7xl mx-auto px-6 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                  CodeForge
                </h1>
                <p className="text-sm text-slate-600 dark:text-slate-400 mt-1.5 font-medium">
                  Self-Improving AI Code Agent • Powered by Google Gemini 2.5
                </p>
              </div>
              <div className="flex items-center space-x-3">
                <ThemeToggle />
                <div className="px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-full text-sm font-semibold shadow-lg">
                  ⚡ Gemini 2.5
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Navigation */}
        <Navigation activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8 pb-24 md:pb-8">
        {activeTab === 'generate' && <Generator />}
        {activeTab === 'patterns' && <PatternLibrary />}
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'self-learning' && <AdvancedSelfLearning />}
      </main>

        {/* Footer */}
        <footer className="bg-white/60 dark:bg-slate-900/60 backdrop-blur-sm border-t border-slate-200/50 dark:border-slate-700/50 mt-16 transition-colors duration-300">
          <div className="max-w-7xl mx-auto px-6 py-6">
            <div className="flex justify-between text-sm text-slate-600 dark:text-slate-400 font-medium">
              <span>🏆 Built for AI Agents Hackathon 2025</span>
              <span>⚡ Multi-Agent A2A • Gemini 2.5 • CopilotKit</span>
            </div>
          </div>
        </footer>

        {/* CopilotKit AI Assistant */}
        <CopilotAssistant />

        {/* Toast Notifications */}
        <Toaster {...toasterConfig} />
      </div>
      </CopilotKitProvider>
    </ThemeProvider>
  );
}

export default App;