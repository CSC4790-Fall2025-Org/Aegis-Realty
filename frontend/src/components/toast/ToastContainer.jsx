import { createPortal } from 'react-dom';
import Toast from './Toast';

const ToastContainer = ({ toasts, removeToast }) => {
  return createPortal(
    <div className="fixed top-4 right-4 z-50 space-y-4 max-w-md w-full flex flex-col items-end">
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          id={toast.id}
          message={toast.message}
          type={toast.type}
          onClose={removeToast}
          duration={toast.duration || 3000}
        />
      ))}
    </div>,
    document.body
  );
};

export default ToastContainer;