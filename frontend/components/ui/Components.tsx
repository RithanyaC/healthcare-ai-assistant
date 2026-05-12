/**
 * Loading Spinner Component
 */
export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center">
      <div className="relative w-6 h-6">
        <div className="absolute inset-0 border-2 border-transparent border-t-blue-500 rounded-full animate-spin"></div>
      </div>
    </div>
  );
}

/**
 * Toast Notification Component
 */
interface ToastProps {
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  onClose: () => void;
}

export function ToastNotification({ message, type, onClose }: ToastProps) {
  const bgColor = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-blue-500',
  }[type];

  const icon = {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ℹ',
  }[type];

  return (
    <div className={`${bgColor} text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 animate-fade-in`}>
      <span className="font-bold text-lg">{icon}</span>
      <span className="flex-1">{message}</span>
      <button
        onClick={onClose}
        className="text-white hover:text-gray-200 font-bold"
      >
        ✕
      </button>
    </div>
  );
}

/**
 * Alert Component
 */
interface AlertProps {
  title: string;
  description?: string;
  type?: 'info' | 'warning' | 'error' | 'success';
  className?: string;
}

export function Alert({
  title,
  description,
  type = 'info',
  className = '',
}: AlertProps) {
  const styles = {
    info: 'bg-blue-50 border border-blue-200 text-blue-800',
    warning: 'bg-yellow-50 border border-yellow-200 text-yellow-800',
    error: 'bg-red-50 border border-red-200 text-red-800',
    success: 'bg-green-50 border border-green-200 text-green-800',
  };

  return (
    <div className={`${styles[type]} rounded-lg p-4 ${className}`}>
      <h3 className="font-semibold">{title}</h3>
      {description && <p className="text-sm mt-1">{description}</p>}
    </div>
  );
}

/**
 * Button Component
 */
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  children,
  disabled,
  ...props
}: ButtonProps) {
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
  };

  const sizes = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      disabled={disabled || loading}
      className={`${variants[variant]} ${sizes[size]} rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2`}
      {...props}
    >
      {loading && <LoadingSpinner />}
      {children}
    </button>
  );
}

/**
 * Card Component
 */
interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export function Card({ children, className = '', ...props }: CardProps) {
  return (
    <div
      className={`bg-white rounded-lg shadow-md p-6 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
