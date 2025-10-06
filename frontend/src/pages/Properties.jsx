import React, { useState, useEffect } from 'react';
import { useInfiniteProperties } from '../hooks/usePropertyQueries.js';

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
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden">
      <div className="p-6">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-lg font-semibold text-gray-900 truncate">
            {formatAddress(property)}
          </h3>
          <span className="text-xl font-bold text-blue-600 ml-4">
            {formatPrice(property.lastSalePrice)}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
          <div>
            <span className="text-gray-600">Bedrooms:</span>
            <span className="ml-2 font-medium">{property.bedrooms || 'N/A'}</span>
          </div>
          <div>
            <span className="text-gray-600">Bathrooms:</span>
            <span className="ml-2 font-medium">{property.bathrooms || 'N/A'}</span>
          </div>
          <div>
            <span className="text-gray-600">Sq Ft:</span>
            <span className="ml-2 font-medium">{property.squareFootage || 'N/A'}</span>
          </div>
          <div>
            <span className="text-gray-600">Year Built:</span>
            <span className="ml-2 font-medium">{property.yearBuilt || 'N/A'}</span>
          </div>
        </div>

        {property.propertyType && (
          <div className="mb-3">
            <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
              {property.propertyType}
            </span>
          </div>
        )}

        <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors duration-200">
          View Details
        </button>
      </div>
    </div>
  );
};

const Properties = () => {
  const [filters] = useState({});

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    error
  } = useInfiniteProperties(filters);

  useEffect(() => {
    // Any side effects can go here
  }, []);

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

  const allProperties = data?.pages?.flat() || [];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Properties</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {allProperties.map((property) => (
          <PropertyCard key={property.id} property={property} />
        ))}
      </div>

      {hasNextPage && (
        <div className="text-center">
          <button
            onClick={() => fetchNextPage()}
            disabled={isFetchingNextPage}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {isFetchingNextPage ? 'Loading...' : 'Load More'}
          </button>
        </div>
      )}

      {allProperties.length === 0 && (
        <div className="text-center text-gray-600">
          No properties found.
        </div>
      )}
    </div>
  );
};

export default Properties;
