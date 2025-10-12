import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotAction, useCopilotReadable } from "@copilotkit/react-core";
import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Bot, X } from "lucide-react";

const CopilotAssistant = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [generatedApps, setGeneratedApps] = useState([]);

  // Make app generation history readable to Copilot
  useCopilotReadable({
    description: "History of generated applications",
    value: generatedApps,
  });

  // Define action for app generation
  useCopilotAction({
    name: "generate_app",
    description: "Generate a web application based on user description",
    parameters: [
      {
        name: "description",
        type: "string",
        description: "Description of the app to generate",
        required: true,
      },
    ],
    handler: async ({ description }) => {
      console.log("Generating app:", description);
      setGeneratedApps(prev => [...prev, { description, timestamp: new Date() }]);
      return `App generation initiated for: ${description}`;
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
