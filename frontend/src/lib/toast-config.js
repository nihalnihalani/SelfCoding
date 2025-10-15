import { toast as sonnerToast } from 'sonner';

// Enhanced toast configurations with custom styling and actions
export const toast = {
  success: (message, options = {}) => {
    return sonnerToast.success(message, {
      duration: 4000,
      className: 'bg-success text-success-foreground',
      ...options,
    });
  },

  error: (message, options = {}) => {
    return sonnerToast.error(message, {
      duration: 5000,
      className: 'bg-error text-error-foreground',
      ...options,
    });
  },

  warning: (message, options = {}) => {
    return sonnerToast.warning(message, {
      duration: 4000,
      className: 'bg-warning text-warning-foreground',
      ...options,
    });
  },

  info: (message, options = {}) => {
    return sonnerToast.info(message, {
      duration: 4000,
      ...options,
    });
  },

  loading: (message, options = {}) => {
    return sonnerToast.loading(message, {
      duration: Infinity,
      ...options,
    });
  },

  promise: (promise, messages, options = {}) => {
    return sonnerToast.promise(promise, {
      loading: messages.loading || 'Loading...',
      success: messages.success || 'Success!',
      error: messages.error || 'Error occurred',
      ...options,
    });
  },

  // Custom toast with action button
  withAction: (message, actionLabel, actionFn, options = {}) => {
    return sonnerToast(message, {
      action: {
        label: actionLabel,
        onClick: actionFn,
      },
      ...options,
    });
  },

  // Dismissible toast with custom duration
  dismissible: (message, duration = 4000, options = {}) => {
    return sonnerToast(message, {
      duration,
      dismissible: true,
      ...options,
    });
  },
};

// Toast configuration for Toaster component
export const toasterConfig = {
  position: 'bottom-right',
  expand: true,
  richColors: true,
  closeButton: true,
  duration: 4000,
  className: 'toaster-custom',
  toastOptions: {
    className: 'toast-custom',
    style: {
      background: 'hsl(var(--card))',
      color: 'hsl(var(--card-foreground))',
      border: '1px solid hsl(var(--border))',
    },
  },
};
