import * as React from "react"
import * as ProgressPrimitive from "@radix-ui/react-progress"
import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

const Progress = React.forwardRef(({ 
  className, 
  value, 
  showPercentage = false,
  gradient = false,
  size = "default",
  ...props 
}, ref) => {
  const sizeClasses = {
    sm: "h-1",
    default: "h-2",
    lg: "h-3",
    xl: "h-4"
  };

  return (
    <div className="w-full">
      <ProgressPrimitive.Root
        ref={ref}
        className={cn(
          "relative w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700",
          sizeClasses[size],
          className
        )}
        {...props}
      >
        <ProgressPrimitive.Indicator
          className={cn(
            "h-full w-full flex-1 transition-all duration-500 ease-out",
            gradient 
              ? "bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" 
              : "bg-primary"
          )}
          style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
        />
      </ProgressPrimitive.Root>
      {showPercentage && (
        <div className="mt-1 text-right text-xs text-slate-600 dark:text-slate-400 font-medium">
          {Math.round(value || 0)}%
        </div>
      )}
    </div>
  );
});
Progress.displayName = ProgressPrimitive.Root.displayName;

// Multi-step progress indicator
const ProgressSteps = ({ steps, currentStep, className }) => {
  return (
    <div className={cn("flex items-center justify-between w-full", className)}>
      {steps.map((step, index) => {
        const isCompleted = index < currentStep;
        const isCurrent = index === currentStep;
        const isPending = index > currentStep;

        return (
          <React.Fragment key={index}>
            <div className="flex flex-col items-center flex-1">
              <motion.div
                initial={false}
                animate={{
                  scale: isCurrent ? 1.1 : 1,
                  backgroundColor: isCompleted 
                    ? "hsl(var(--success))" 
                    : isCurrent 
                    ? "hsl(var(--primary))" 
                    : "hsl(var(--muted))"
                }}
                transition={{ duration: 0.3 }}
                className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center text-white font-semibold text-sm",
                  "border-2",
                  isCompleted && "border-success",
                  isCurrent && "border-primary",
                  isPending && "border-slate-300 dark:border-slate-600"
                )}
              >
                {isCompleted ? "✓" : index + 1}
              </motion.div>
              <div className={cn(
                "mt-2 text-xs font-medium text-center",
                isCompleted && "text-success",
                isCurrent && "text-primary",
                isPending && "text-slate-400 dark:text-slate-500"
              )}>
                {step.label}
              </div>
              {step.description && (
                <div className="mt-1 text-xs text-slate-500 dark:text-slate-400 text-center max-w-[100px]">
                  {step.description}
                </div>
              )}
            </div>
            {index < steps.length - 1 && (
              <div className="flex-1 h-0.5 mx-2 mb-6">
                <div className={cn(
                  "h-full transition-all duration-500",
                  index < currentStep 
                    ? "bg-success" 
                    : "bg-slate-300 dark:bg-slate-600"
                )} />
              </div>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};

// Circular progress indicator
const CircularProgress = ({ value = 0, size = 120, strokeWidth = 8, className }) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className={cn("relative inline-flex items-center justify-center", className)}>
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="none"
          className="text-slate-200 dark:text-slate-700"
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="url(#gradient)"
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: "easeInOut" }}
          style={{
            strokeDasharray: circumference,
          }}
        />
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="hsl(var(--primary))" />
            <stop offset="100%" stopColor="hsl(var(--secondary))" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-2xl font-bold text-slate-800 dark:text-slate-200">
          {Math.round(value)}%
        </span>
      </div>
    </div>
  );
};

export { Progress, ProgressSteps, CircularProgress }
