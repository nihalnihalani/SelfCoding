import { motion } from 'framer-motion';
import { Rocket, Library, BarChart3, Brain, Menu, X } from 'lucide-react';
import { useState, useEffect } from 'react';
import { cn } from '@/lib/utils';

const navItems = [
  { id: 'generate', label: 'Generate', icon: Rocket, emoji: '🚀' },
  { id: 'patterns', label: 'Pattern Library', icon: Library, emoji: '📚' },
  { id: 'dashboard', label: 'Dashboard', icon: BarChart3, emoji: '📊' },
  { id: 'self-learning', label: 'Advanced Learning', icon: Brain, emoji: '🧠' },
];

const Navigation = ({ activeTab, onTabChange }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const handleTabChange = (tabId) => {
    onTabChange(tabId);
    setIsMobileMenuOpen(false);
  };

  const handleKeyDown = (e, tabId) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleTabChange(tabId);
    }
    
    // Arrow key navigation
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
      e.preventDefault();
      const currentIndex = navItems.findIndex(item => item.id === activeTab);
      const nextIndex = e.key === 'ArrowRight' 
        ? (currentIndex + 1) % navItems.length 
        : (currentIndex - 1 + navItems.length) % navItems.length;
      handleTabChange(navItems[nextIndex].id);
    }
  };

  // Desktop Navigation
  if (!isMobile) {
    return (
      <nav className="bg-white/60 dark:bg-slate-900/60 backdrop-blur-sm border-b border-slate-200/50 dark:border-slate-700/50 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex space-x-1" role="tablist">
            {navItems.map((item) => {
              const isActive = activeTab === item.id;
              
              return (
                <button
                  key={item.id}
                  data-testid={`nav-${item.id}`}
                  onClick={() => handleTabChange(item.id)}
                  onKeyDown={(e) => handleKeyDown(e, item.id)}
                  role="tab"
                  aria-selected={isActive}
                  aria-controls={`panel-${item.id}`}
                  tabIndex={isActive ? 0 : -1}
                  className={cn(
                    "py-4 px-6 font-semibold text-sm transition-all duration-200 relative group",
                    isActive
                      ? 'text-indigo-600 dark:text-indigo-400'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'
                  )}
                >
                  <span className="relative z-10 flex items-center space-x-2">
                    <span>{item.emoji}</span>
                    <span>{item.label}</span>
                  </span>
                  
                  {/* Hover effect */}
                  {!isActive && (
                    <motion.div
                      className="absolute inset-0 bg-slate-100 dark:bg-slate-800 rounded-t-lg opacity-0 group-hover:opacity-100"
                      initial={false}
                      transition={{ duration: 0.2 }}
                    />
                  )}
                  
                  {/* Active indicator with smooth animation */}
                  {isActive && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-indigo-600 to-purple-600"
                      transition={{ type: "spring", stiffness: 500, damping: 30 }}
                    />
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </nav>
    );
  }

  // Mobile Navigation
  return (
    <>
      {/* Mobile Header with Menu Button */}
      <nav className="bg-white/60 dark:bg-slate-900/60 backdrop-blur-sm border-b border-slate-200/50 dark:border-slate-700/50 transition-colors duration-300 md:hidden">
        <div className="px-4 py-3 flex items-center justify-between">
          <div className="text-sm font-semibold text-slate-800 dark:text-slate-200">
            {navItems.find(item => item.id === activeTab)?.label}
          </div>
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            aria-label="Toggle menu"
            aria-expanded={isMobileMenuOpen}
          >
            {isMobileMenuOpen ? (
              <X className="w-5 h-5 text-slate-600 dark:text-slate-400" />
            ) : (
              <Menu className="w-5 h-5 text-slate-600 dark:text-slate-400" />
            )}
          </button>
        </div>
      </nav>

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Mobile Menu Drawer */}
      <motion.div
        initial={{ x: '-100%' }}
        animate={{ x: isMobileMenuOpen ? 0 : '-100%' }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        className="fixed top-0 left-0 bottom-0 w-64 bg-white dark:bg-slate-900 shadow-xl z-50 md:hidden"
      >
        <div className="p-6">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-lg font-bold text-slate-800 dark:text-slate-200">Menu</h2>
            <button
              onClick={() => setIsMobileMenuOpen(false)}
              className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              aria-label="Close menu"
            >
              <X className="w-5 h-5 text-slate-600 dark:text-slate-400" />
            </button>
          </div>
          
          <div className="space-y-2">
            {navItems.map((item) => {
              const isActive = activeTab === item.id;
              const Icon = item.icon;
              
              return (
                <button
                  key={item.id}
                  onClick={() => handleTabChange(item.id)}
                  className={cn(
                    "w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200",
                    isActive
                      ? 'bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                  )}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </motion.div>

      {/* Mobile Bottom Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-t border-slate-200 dark:border-slate-700 z-30 md:hidden">
        <div className="flex items-center justify-around px-2 py-2">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            const Icon = item.icon;
            
            return (
              <button
                key={item.id}
                onClick={() => handleTabChange(item.id)}
                className={cn(
                  "flex flex-col items-center justify-center px-3 py-2 rounded-lg transition-all duration-200 min-w-[60px]",
                  isActive
                    ? 'text-indigo-600 dark:text-indigo-400'
                    : 'text-slate-500 dark:text-slate-400'
                )}
                aria-label={item.label}
              >
                <Icon className={cn(
                  "w-6 h-6 transition-transform duration-200",
                  isActive && "scale-110"
                )} />
                <span className={cn(
                  "text-xs mt-1 font-medium transition-all duration-200",
                  isActive ? "opacity-100" : "opacity-0"
                )}>
                  {item.label.split(' ')[0]}
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default Navigation;
