import { useState, useEffect, useRef } from 'react';
import { FiTrendingUp, FiShield, FiZap, FiSearch } from 'react-icons/fi';
import { searchPropertiesByAddress } from '../../services/propertyServices.js';
import { useNavigate } from 'react-router-dom';

const HeroSection = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const containerRef = useRef(null);

  useEffect(() => {
    const handler = setTimeout(async () => {
      const q = query.trim();
      if (q.length < 3) {
        setResults([]);
        setOpen(false);
        return;
      }
      try {
        setLoading(true);
        const data = await searchPropertiesByAddress(q, 8);
        setResults(data || []);
        setOpen((data || []).length > 0);
      } catch (e) {
        setResults([]);
        setOpen(false);
      } finally {
        setLoading(false);
      }
    }, 250);
    return () => clearTimeout(handler);
  }, [query]);

  useEffect(() => {
    const onClick = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('click', onClick);
    return () => document.removeEventListener('click', onClick);
  }, []);
  return (
    <section className="relative py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-text mb-6">
            Revolutionize Your
            <span className="text-primary block">Real Estate Investment</span>
          </h1>

          <p className="text-xl text-muted max-w-3xl mx-auto mb-8">
            Leverage AI-powered insights and comprehensive analysis to make smarter property investment decisions.
            From instant cash flow projections to automated property management - all in one platform
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <div className="flex items-center space-x-2 text-primary">
              <FiTrendingUp className="w-5 h-5" />
              <span>AI-Powered Analysis</span>
            </div>
            <div className="flex items-center space-x-2 text-primary">
              <FiShield className="w-5 h-5" />
              <span>Risk Assessment</span>
            </div>
            <div className="flex items-center space-x-2 text-primary">
              <FiZap className="w-5 h-5" />
              <span>Instant Reports</span>
            </div>
          </div>

          <div ref={containerRef} className="bg-background backdrop-blur-sm rounded-lg shadow-lg p-6 max-w-md mx-auto">
            <h3 className="text-lg font-semibold text-text mb-4">Start Your Analysis</h3>
            <div className="relative">
              <div className="flex items-center gap-2">
                <FiSearch className="text-text/60" />
                <input
                  type="text"
                  placeholder="Enter property address..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onFocus={() => results.length > 0 && setOpen(true)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>

              {open && (
                <div className="absolute left-0 right-0 mt-2 bg-background border border-border/30 rounded-lg shadow-lg overflow-hidden z-10">
                  {loading && (
                    <div className="px-4 py-3 text-sm text-text/70">Searching…</div>
                  )}
                  {!loading && results.length === 0 && (
                    <div className="px-4 py-3 text-sm text-text/70">No matches</div>
                  )}
                  {!loading && results.map((p) => (
                    <button
                      key={p.id}
                      onClick={() => navigate(`/properties/${p.id}`)}
                      className="w-full text-left px-4 py-3 hover:bg-secondary cursor-pointer"
                    >
                      <div className="text-sm font-medium text-text">
                        {p.formattedAddress || `${p.addressLine1 || ''} ${p.city || ''}, ${p.state || ''} ${p.zipCode || ''}`}
                      </div>
                      <div className="text-xs text-text/70">
                        {p.propertyType || 'Property'} • {p.squareFootage ? `${p.squareFootage} sqft` : 'Size N/A'} • {p.lastSalePrice ? new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(p.lastSalePrice) : 'Price N/A'}
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;