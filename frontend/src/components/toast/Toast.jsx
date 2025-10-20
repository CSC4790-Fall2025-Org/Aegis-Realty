import { useState, useEffect } from 'react';
import { IoClose } from 'react-icons/io5';

const Toast = ({ id, message, type = 'info', onClose, duration = 3000 }) => {
  const [progress, setProgress] = useState(100);
  const [intervalId, setIntervalId] = useState(null);

  useEffect(() => {
    // Start progress bar countdown
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev <= 0) {
          clearInterval(interval);
          onClose(id);
          return 0;
        }
        // Decrease by percentage points based on duration
        return prev - (100 / (duration / 100));
      });
    }, 100);

    setIntervalId(interval);

    return () => {
      clearInterval(interval);
    };
  }, [id, duration, onClose]);

  const handleClose = () => {
    if (intervalId) clearInterval(intervalId);
    onClose(id);
  };

  const bgColors = {
    success: 'bg-green-100 border-green-500 text-green-800',
    error: 'bg-red-100 border-red-500 text-red-800',
    warning: 'bg-yellow-100 border-yellow-500 text-yellow-800',
    info: 'bg-blue-100 border-blue-500 text-blue-800',
  };

  return (
    <div className={`max-w-sm w-full shadow-lg rounded-lg pointer-events-auto border-l-4 ${bgColors[type]}`}>
      <div className="p-4">
        <div className="flex items-start">
          <div className="ml-3 w-0 flex-1">
            <p className="text-sm font-medium">{message}</p>
          </div>
          <div className="ml-4 flex-shrink-0 flex">
            <button
              onClick={handleClose}
              className="inline-flex text-gray-400 hover:text-gray-500 focus:outline-none"
            >
              <IoClose className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
      <div
        className={`h-1 ${
          type === 'success' 
            ? 'bg-green-500' 
            : type === 'error' 
              ? 'bg-red-500' 
              : type === 'warning' 
                ? 'bg-yellow-500' 
                : 'bg-blue-500'
        }`}
        style={{ width: `${progress}%`, transition: 'width 100ms linear' }}
      />
    </div>
  );
};

export default Toast;