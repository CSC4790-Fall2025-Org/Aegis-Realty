import React, { useState } from 'react';

/**
 * PropertySearchForm
 * Props:
 * - onSearch: (address: string) => Promise<void> | void
 * - isLoading?: boolean
 * - error?: string | null
 */
const PropertySearchForm = ({ onSearch, isLoading = false, error = null }) => {
  const [address, setAddress] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmed = address.trim();
    if (!trimmed) return;
    await onSearch?.(trimmed);
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <label htmlFor="address" className="text-sm font-medium text-text">Property address</label>
        <div className="flex gap-2">
          <input
            id="address"
            type="text"
            placeholder="e.g., 123 Main St, City, ST 12345"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            className="flex-1 rounded-md border border-neutral-300 bg-white px-3 py-2 shadow-sm focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/30"
            disabled={isLoading}
            autoComplete="street-address"
          />
          <button
            type="submit"
            disabled={isLoading || !address.trim()}
            className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 font-semibold text-white shadow hover:bg-primary/90 disabled:opacity-50"
          >
            {isLoading ? 'Analyzing…' : 'Analyze'}
          </button>
        </div>
        {error ? (
          <p className="text-sm text-red-600">{error}</p>
        ) : (
          <p className="text-xs text-muted">Enter a full mailing address for best results.</p>
        )}
      </form>
    </div>
  );
};

export default PropertySearchForm;
