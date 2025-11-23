const DesktopNav = ({ onNavigate }) => {
  const navItems = [
    { label: 'Home', path: '/' },
    { label: 'Properties', path: '/properties' },
    { label: 'Analysis', path: '/analysis' },
  ];

  return (
    <nav className="hidden md:flex items-center space-x-6">
      {navItems.map(({ label, path }) => (
        <button
          key={path}
          onClick={() => onNavigate(path)}
          className="text-text hover:text-primary transition-colors cursor-pointer"
        >
          {label}
        </button>
      ))}
    </nav>
  );
};

export default DesktopNav;