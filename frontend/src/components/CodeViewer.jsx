import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Copy, Check } from 'lucide-react';
import { toast } from 'sonner';

const CodeViewer = ({ files }) => {
  const [selectedFile, setSelectedFile] = useState(Object.keys(files)[0]);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(files[selectedFile]);
    setCopied(true);
    toast.success('Code copied to clipboard!');
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Card data-testid="code-viewer-card" className="border-slate-200 shadow-lg overflow-hidden">
      <CardHeader className="bg-slate-50 border-b border-slate-200">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg flex items-center space-x-2">
            <span>📄</span>
            <span>Generated Code</span>
          </CardTitle>
          <Button
            data-testid="copy-code-button"
            onClick={handleCopy}
            variant="outline"
            size="sm"
            className="flex items-center space-x-2"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                <span>Copy</span>
              </>
            )}
          </Button>
        </div>
        <div className="flex flex-wrap gap-2 mt-4">
          {Object.keys(files).map((filename) => (
            <button
              key={filename}
              data-testid={`file-tab-${filename}`}
              onClick={() => setSelectedFile(filename)}
              className={`px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                selectedFile === filename
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-white text-slate-700 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              {filename}
            </button>
          ))}
        </div>
      </CardHeader>
      
      <CardContent className="p-0">
        <div className="max-h-[500px] overflow-auto bg-slate-900">
          <pre className="p-6 text-sm">
            <code className="text-slate-100 font-mono">{files[selectedFile]}</code>
          </pre>
        </div>
      </CardContent>
    </Card>
  );
};

export default CodeViewer;