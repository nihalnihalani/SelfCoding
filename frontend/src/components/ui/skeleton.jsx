import { cn } from "@/lib/utils";

function Skeleton({ className, ...props }) {
  return (
    <div
      className={cn(
        "animate-shimmer rounded-md bg-gradient-to-r from-slate-200 via-slate-100 to-slate-200 dark:from-slate-800 dark:via-slate-700 dark:to-slate-800",
        "bg-[length:200%_100%]",
        className
      )}
      {...props}
    />
  );
}

// Skeleton variants for different content types
const SkeletonCard = ({ className }) => (
  <div className={cn("rounded-lg border border-slate-200 dark:border-slate-700 p-6 space-y-4", className)}>
    <Skeleton className="h-4 w-3/4" />
    <Skeleton className="h-4 w-1/2" />
    <Skeleton className="h-20 w-full" />
  </div>
);

const SkeletonChart = ({ className }) => (
  <div className={cn("rounded-lg border border-slate-200 dark:border-slate-700 p-6 space-y-4", className)}>
    <Skeleton className="h-6 w-1/3" />
    <Skeleton className="h-64 w-full" />
    <div className="flex justify-between">
      <Skeleton className="h-4 w-20" />
      <Skeleton className="h-4 w-20" />
    </div>
  </div>
);

const SkeletonTable = ({ rows = 5, className }) => (
  <div className={cn("rounded-lg border border-slate-200 dark:border-slate-700 overflow-hidden", className)}>
    <div className="bg-slate-50 dark:bg-slate-800 p-4 border-b border-slate-200 dark:border-slate-700">
      <div className="flex space-x-4">
        <Skeleton className="h-4 w-1/4" />
        <Skeleton className="h-4 w-1/4" />
        <Skeleton className="h-4 w-1/4" />
        <Skeleton className="h-4 w-1/4" />
      </div>
    </div>
    <div className="divide-y divide-slate-200 dark:divide-slate-700">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="p-4 flex space-x-4">
          <Skeleton className="h-4 w-1/4" />
          <Skeleton className="h-4 w-1/4" />
          <Skeleton className="h-4 w-1/4" />
          <Skeleton className="h-4 w-1/4" />
        </div>
      ))}
    </div>
  </div>
);

const SkeletonText = ({ lines = 3, className }) => (
  <div className={cn("space-y-2", className)}>
    {Array.from({ length: lines }).map((_, i) => (
      <Skeleton 
        key={i} 
        className={cn(
          "h-4",
          i === lines - 1 ? "w-3/4" : "w-full"
        )} 
      />
    ))}
  </div>
);

const SkeletonMetricCard = ({ className }) => (
  <div className={cn("rounded-lg border border-slate-200 dark:border-slate-700 p-6 space-y-3", className)}>
    <div className="flex items-center justify-between">
      <Skeleton className="h-4 w-24" />
      <Skeleton className="h-5 w-5 rounded-full" />
    </div>
    <Skeleton className="h-8 w-20" />
    <Skeleton className="h-3 w-16" />
  </div>
);

const SkeletonAvatar = ({ className }) => (
  <Skeleton className={cn("h-10 w-10 rounded-full", className)} />
);

const SkeletonButton = ({ className }) => (
  <Skeleton className={cn("h-10 w-24 rounded-md", className)} />
);

export { 
  Skeleton, 
  SkeletonCard, 
  SkeletonChart, 
  SkeletonTable, 
  SkeletonText,
  SkeletonMetricCard,
  SkeletonAvatar,
  SkeletonButton
};
