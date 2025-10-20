const Spinner = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'h-36 w-36',
    md: 'h-48 w-48',
    lg: 'h-60 w-60',
  };

  return (
    <div className={`${className} flex justify-center items-center`}>
      <div className={`animate-spin rounded-full border-t-2 border-b-2 border-primary ${sizeClasses[size]}`}></div>
    </div>
  );
};

export default Spinner;