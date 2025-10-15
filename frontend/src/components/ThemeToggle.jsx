import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { Button } from './ui/button';
import { motion } from 'framer-motion';

const ThemeToggle = () => {
  const { theme, setTheme, actualTheme } = useTheme();

  const toggleTheme = () => {
    if (theme === 'system') {
      setTheme(actualTheme === 'dark' ? 'light' : 'dark');
    } else {
      setTheme(theme === 'dark' ? 'light' : 'dark');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleTheme();
    }
  };

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={toggleTheme}
      onKeyDown={handleKeyDown}
      className="relative overflow-hidden transition-colors duration-300"
      aria-label={`Switch to ${actualTheme === 'dark' ? 'light' : 'dark'} mode`}
      title={`Switch to ${actualTheme === 'dark' ? 'light' : 'dark'} mode`}
    >
      <motion.div
        initial={false}
        animate={{
          scale: actualTheme === 'dark' ? 0 : 1,
          rotate: actualTheme === 'dark' ? 90 : 0,
          opacity: actualTheme === 'dark' ? 0 : 1,
        }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="absolute"
      >
        <Sun className="h-[1.2rem] w-[1.2rem]" />
      </motion.div>
      <motion.div
        initial={false}
        animate={{
          scale: actualTheme === 'dark' ? 1 : 0,
          rotate: actualTheme === 'dark' ? 0 : -90,
          opacity: actualTheme === 'dark' ? 1 : 0,
        }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="absolute"
      >
        <Moon className="h-[1.2rem] w-[1.2rem]" />
      </motion.div>
    </Button>
  );
};

export default ThemeToggle;
