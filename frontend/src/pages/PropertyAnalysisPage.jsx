import React, { useState } from 'react';
import PropertySearchForm from '../components/PropertySearchForm.jsx';
import AnalysisReportDisplay from '../components/AnalysisReportDisplay.jsx';
import { createProperty, analyzeProperty } from '../services/propertyServices.js';

const PropertyAnalysisPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [report, setReport] = useState(null);

  const handleSearch = async (address) => {
    setError(null);
    setReport(null);
    setIsLoading(true);

    try {
      // 1) Create a minimal property with just the formatted address
      const created = await createProperty({ formatted_address: address });
      if (!created?.id) {
        throw new Error('Failed to create property');
      }

      // 2) Request analysis for that property id (defaults: gross mode, 8% threshold)
      const analysis = await analyzeProperty(created.id, {
        address,
        calculation_mode: 'gross',
        cap_rate_threshold: 8.0,
      });

      setReport(analysis);
    } catch (e) {
      const message = e?.response?.data?.detail || e?.message || 'An unexpected error occurred';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-8">
      <div className="mb-6 text-center">
        <h1 className="text-2xl font-bold">Property Investment Analysis</h1>
        <p className="mt-1 text-sm text-neutral-600">Enter a property address to generate a comprehensive analysis.</p>
      </div>

      <PropertySearchForm onSearch={handleSearch} isLoading={isLoading} error={error} />

      {isLoading && (
        <div className="mt-6 text-center text-sm text-neutral-600">Generating analysis…</div>
      )}

      {!isLoading && report && (
        <AnalysisReportDisplay report={report} />
      )}
    </div>
  );
};

export default PropertyAnalysisPage;
