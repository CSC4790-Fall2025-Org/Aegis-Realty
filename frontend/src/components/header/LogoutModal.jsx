const LogoutModal = ({ isOpen, onConfirm, onCancel }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
      <div className="bg-secondary p-6 rounded-lg shadow-xl max-w-sm w-full mx-4">
        <h3 className="text-xl font-bold text-text mb-4">Confirm Logout</h3>
        <p className="text-text mb-6">Are you sure you want to logout?</p>
        <div className="flex space-x-4">
          <button
            onClick={onConfirm}
            className="flex-1 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors cursor-pointer"
          >
            Logout
          </button>
          <button
            onClick={onCancel}
            className="flex-1 bg-gray-300 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-400 transition-colors cursor-pointer"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default LogoutModal;