import React, { useState, useMemo } from 'react';
import { FiFilter, FiX, FiChevronDown, FiChevronUp } from 'react-icons/fi';
import { useInfiniteProperties } from '../hooks/usePropertyQueries.js';
import { getPropertyImage } from '../utils/imageHelper';
import { useAuth } from '../contexts/AuthContext';

const FilterPanel = ({ filters, setFilters, onClear }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="bg-background rounded-lg shadow-md p-6 mb-6">
      <div className="flex items-center justify-between ">
        <h2 className="text-xl font-bold text-text flex items-center gap-2">
          <FiFilter size={20} />
          Filters
        </h2>
        <div className="flex gap-2">
          <button
            onClick={onClear}
            className="text-sm text-primary hover:text-primary/70 flex items-center gap-1 cursor-pointer"
          >
            <FiX size={16} />
            Clear All
          </button>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-text cursor-pointer"
          >
            {isExpanded ? <FiChevronUp size={20} /> : <FiChevronDown size={20} />}
          </button>
        </div>
      </div>

      {isExpanded && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-text mb-2">Min Bedrooms</label>
            <input
              type="number"
              min="0"
              value={filters.minBedrooms || ''}
              onChange={(e) => handleFilterChange('minBedrooms', e.target.value)}
              placeholder="Any"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text mb-2">Min Bathrooms</label>
            <input
              type="number"
              min="0"
              step="0.5"
              value={filters.minBathrooms || ''}
              onChange={(e) => handleFilterChange('minBathrooms', e.target.value)}
              placeholder="Any"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text mb-2">Min Sq Ft</label>
            <input
              type="number"
              min="0"
              value={filters.minSquareFootage || ''}
              onChange={(e) => handleFilterChange('minSquareFootage', e.target.value)}
              placeholder="Any"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text mb-2">Max Sq Ft</label>
            <input
              type="number"
              min="0"
              value={filters.maxSquareFootage || ''}
              onChange={(e) => handleFilterChange('maxSquareFootage', e.target.value)}
              placeholder="Any"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text mb-2">Min Price</label>
            <input
              type="number"
              min="0"
              value={filters.minPrice || ''}
              onChange={(e) => handleFilterChange('minPrice', e.target.value)}
              placeholder="Any"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text mb-2">Max Price</label>
            <input
              type="number"
              min="0"
              value={filters.maxPrice || ''}
              onChange={(e) => handleFilterChange('maxPrice', e.target.value)}
              placeholder="Any"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text mb-2">Sort By</label>
            <div className="flex gap-2">
              <select
                value={filters.sortBy || ''}
                onChange={(e) => handleFilterChange('sortBy', e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
              >
                <option value="">None</option>
                <option value="bedrooms">Bedrooms</option>
                <option value="bathrooms">Bathrooms</option>
                <option value="squareFootage">Square Footage</option>
                <option value="lastSalePrice">Price</option>
                <option value="yearBuilt">Year Built</option>
              </select>
              {filters.sortBy && (
                <select
                  value={filters.sortOrder || 'asc'}
                  onChange={(e) => handleFilterChange('sortOrder', e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
                >
                  <option value="asc">Asc</option>
                  <option value="desc">Desc</option>
                </select>
              )}
            </div>
          </div>

          <div className="flex items-end">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={filters.favoritesOnly || false}
                onChange={(e) => handleFilterChange('favoritesOnly', e.target.checked)}
                className="w-4 h-4 text-primary focus:ring-2 focus:ring-primary cursor-pointer"
              />
              <span className="text-sm font-medium text-text">Favorites Only</span>
            </label>
          </div>
        </div>
      )}
    </div>
  );
};

const PropertyCard = ({ property }) => {
  const formatPrice = (price) => {
    if (!price) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const formatAddress = (property) => {
    return property.formattedAddress ||
           `${property.addressLine1 || ''} ${property.city || ''}, ${property.state || ''} ${property.zipCode || ''}`.trim();
  };

  return (
    <div className="bg-background rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden">
      <img
        src={getPropertyImage(property)}
        alt="property image"
        className="w-full h-48 object-cover"
      />

      <div className="p-6">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-lg font-semibold text-text truncate">
            {formatAddress(property)}
          </h3>
          <span className="text-xl font-bold text-text ml-4">
            {formatPrice(property.lastSalePrice)}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
          <div>
            <span className="text-text">Bedrooms:</span>
            <span className="ml-2 text-text font-medium">{property.bedrooms || 'N/A'}</span>
          </div>
          <div>
            <span className="text-text">Bathrooms:</span>
            <span className="ml-2 text-text font-medium">{property.bathrooms || 'N/A'}</span>
          </div>
          <div>
            <span className="text-text">Sq Ft:</span>
            <span className="ml-2 text-text font-medium">{property.squareFootage || 'N/A'}</span>
          </div>
          <div>
            <span className="text-text">Year Built:</span>
            <span className="ml-2 text-text font-medium">{property.yearBuilt || 'N/A'}</span>
          </div>
        </div>

        {property.propertyType && (
          <div className="mb-3">
            <span className="inline-block bg-primary text-text text-xs px-2 py-1 rounded-full">
              {property.propertyType}
            </span>
          </div>
        )}

        <button className="w-full bg-primary text-white py-2 px-4 rounded-md hover:bg-primary/70 transition-colors duration-200 cursor-pointer">
          View Details
        </button>
      </div>
    </div>
  );
};

const Properties = () => {
  const { currentUser } = useAuth();
  const [filters, setFilters] = useState({
    minBedrooms: '',
    minBathrooms: '',
    minSquareFootage: '',
    maxSquareFootage: '',
    minPrice: '',
    maxPrice: '',
    sortBy: '',
    sortOrder: 'asc',
    favoritesOnly: false
  });

  const { data, fetchNextPage, hasNextPage, isFetchingNextPage, isLoading, error } = useInfiniteProperties();

  const allProperties = data?.pages?.flat() || [];

  const filteredAndSortedProperties = useMemo(() => {
    let result = [...allProperties];

    if (filters.favoritesOnly) {
      const favoriteIds = currentUser?.favorite_properties || [];
      console.log('Favorites filter active:', { favoriteIds, currentUser }); // Debug log
      result = result.filter(p => favoriteIds.includes(p.id));
    }

    if (filters.minBedrooms) {
      result = result.filter(p => (p.bedrooms || 0) >= Number(filters.minBedrooms));
    }

    if (filters.minBathrooms) {
      result = result.filter(p => (p.bathrooms || 0) >= Number(filters.minBathrooms));
    }

    if (filters.minSquareFootage) {
      result = result.filter(p => (p.squareFootage || 0) >= Number(filters.minSquareFootage));
    }
    if (filters.maxSquareFootage) {
      result = result.filter(p => (p.squareFootage || 0) <= Number(filters.maxSquareFootage));
    }

    if (filters.minPrice) {
      result = result.filter(p => (p.lastSalePrice || 0) >= Number(filters.minPrice));
    }
    if (filters.maxPrice) {
      result = result.filter(p => (p.lastSalePrice || 0) <= Number(filters.maxPrice));
    }

    if (filters.sortBy) {
      result.sort((a, b) => {
        const aVal = a[filters.sortBy] || 0;
        const bVal = b[filters.sortBy] || 0;
        return filters.sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
      });
    }

    return result;
  }, [allProperties, filters, currentUser?.favorite_properties]);

  const handleClearFilters = () => {
    setFilters({
      minBedrooms: '',
      minBathrooms: '',
      minSquareFootage: '',
      maxSquareFootage: '',
      minPrice: '',
      maxPrice: '',
      sortBy: '',
      sortOrder: 'asc',
      favoritesOnly: false
    });
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">Loading properties...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-red-600">
          Error loading properties: {error.message}
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-text mb-8">Properties</h1>

      <FilterPanel
        filters={filters}
        setFilters={setFilters}
        onClear={handleClearFilters}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {filteredAndSortedProperties.map((property) => (
          <PropertyCard key={property.id} property={property} />
        ))}
      </div>

      {hasNextPage && (
        <div className="text-center">
          <button
            onClick={() => fetchNextPage()}
            disabled={isFetchingNextPage}
            className="bg-primary text-white px-6 py-2 mb-2 rounded-md hover:bg-primary/70 disabled:opacity-50 cursor-pointer"
          >
            {isFetchingNextPage ? 'Loading...' : 'Load More'}
          </button>
        </div>
      )}

      {filteredAndSortedProperties.length === 0 && (
        <div className="text-center text-text">
          No properties found matching your filters
        </div>
      )}
    </div>
  );
};

export default Properties;