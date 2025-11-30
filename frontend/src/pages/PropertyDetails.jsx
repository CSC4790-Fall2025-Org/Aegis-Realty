import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useProperty } from '../hooks/usePropertyQueries.js';
import { getPropertyImage } from '../utils/imageHelper';

const Stat = ({ label, value }) => (
  <div className="flex flex-col items-start bg-secondary rounded-md p-3 border border-border/30">
    <span className="text-xs uppercase tracking-wide text-text/60">{label}</span>
    <span className="text-base font-semibold text-text">{value ?? 'N/A'}</span>
  </div>
);

const Section = ({ title, children }) => (
  <div className="bg-background rounded-lg shadow-sm border border-border/30 p-6">
    <h3 className="text-lg font-semibold text-text mb-4">{title}</h3>
    {children}
  </div>
);

const formatCurrency = (val) => {
  if (val === null || val === undefined || val === '') return 'N/A';
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(Number(val));
};

const PropertyDetails = () => {
  const { id } = useParams();
  const { data: property, isLoading, error } = useProperty(id);

  if (isLoading) return <div className="container mx-auto px-4 py-8">Loading property...</div>;
  if (error) return <div className="container mx-auto px-4 py-8 text-red-600">Error: {error.message}</div>;
  if (!property) return <div className="container mx-auto px-4 py-8">Property not found.</div>;

  const address = property.formattedAddress || [property.addressLine1, property.city, property.state, property.zipCode].filter(Boolean).join(', ');

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl md:text-3xl font-bold text-text">Property Details</h1>
        <Link to="/properties" className="text-primary hover:underline text-sm md:text-base">← Back to Properties</Link>
      </div>

      {/* Hero */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2 overflow-hidden rounded-xl shadow-md border border-border/30">
          <img src={getPropertyImage(property)} alt="property" className="w-full h-[320px] md:h-[420px] object-cover" />
        </div>
        <div className="lg:col-span-1 bg-background rounded-xl shadow-md border border-border/30 p-6 flex flex-col gap-3">
          <h2 className="text-xl font-semibold text-text leading-snug">{address}</h2>
          {property.propertyType && (
            <span className="inline-block w-fit bg-primary text-white text-xs px-2 py-1 rounded-full">{property.propertyType}</span>
          )}
          <div className="grid grid-cols-2 gap-3 mt-2">
            <Stat label="Price" value={formatCurrency(property.lastSalePrice)} />
            <Stat label="Sq Ft" value={property.squareFootage} />
            <Stat label="Beds" value={property.bedrooms} />
            <Stat label="Baths" value={property.bathrooms} />
            <Stat label="Year" value={property.yearBuilt} />
            <Stat label="Lot (sqft)" value={property.lotSize} />
          </div>
        </div>
      </div>

      {/* Details Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Key Facts */}
        <Section title="Key Facts">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Stat label="Stories" value={property.stories} />
            <Stat label="Parking" value={property.parkingSpaces} />
            <Stat label="Garage" value={property.garageSpaces} />
            <Stat label="Pool" value={property.pool ? 'Yes' : 'No'} />
            <Stat label="Status" value={property.listingStatus} />
          </div>
        </Section>

        {/* Financial */}
        <Section title="Financial">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Stat label="Estimated Value" value={formatCurrency(property.estimatedValue)} />
            <Stat label="Assessed Value" value={formatCurrency(property.assessedValue)} />
            <Stat label="Annual Taxes" value={formatCurrency(property.annualPropertyTaxes)} />
            <Stat label="HOA Dues" value={formatCurrency(property.hoaDues)} />
            <Stat label="Insurance" value={formatCurrency(property.insurance)} />
          </div>
        </Section>

        {/* Location */}
        <Section title="Location">
          <div className="text-sm text-text/80">
            <p className="mb-2"><span className="font-medium text-text">Address:</span> {address}</p>
            <p className="mb-2"><span className="font-medium text-text">County:</span> {property.county || 'N/A'}</p>
            <p className="mb-2"><span className="font-medium text-text">APN:</span> {property.parcelNumber || 'N/A'}</p>
          </div>
        </Section>
      </div>

      {/* Raw JSON (collapsible) */}
      <details className="mt-8 bg-background rounded-lg shadow-sm border border-border/30">
        <summary className="cursor-pointer select-none px-6 py-3 text-sm text-text/70 hover:text-text">Developer Data</summary>
        <pre className="px-6 pb-6 text-xs overflow-auto max-h-80 whitespace-pre-wrap text-text/80">{JSON.stringify(property, null, 2)}</pre>
      </details>
    </div>
  );
};

export default PropertyDetails;
