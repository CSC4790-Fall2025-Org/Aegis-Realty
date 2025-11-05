import React from 'react';

/**
 * AnalysisReportDisplay
 * Props:
 * - report: {
 *    property_data: {...},
 *    financial_analysis: {
 *      property_value: number,
 *      rent_estimates: { rent: number, rent_low: number, rent_high: number },
 *      cap_rates: { low: number, mid: number, high: number } | { error?: string },
 *      recommendation: { decision: string, reason: string },
 *      calculation_mode: 'gross' | 'net',
 *      meets_threshold?: Record<string, boolean>,
 *      api_calls_remaining?: number,
 *      expenses_used?: Record<string, number>
 *    },
 *    ai_analysis: { investment_analysis?: any }
 *  }
 */
const AnalysisReportDisplay = ({ report }) => {
  if (!report) return null;

  const { property_data, financial_analysis, ai_analysis } = report || {};
  const property = property_data || {};
  const fin = financial_analysis || {};
  const rents = fin.rent_estimates || {};
  const caps = fin.cap_rates || {};
  const rec = fin.recommendation || {};
  const ai = (ai_analysis && (ai_analysis.investment_analysis || ai_analysis)) || null;

  const CapBadge = ({ ok }) => (
    <span className={`px-2 py-0.5 rounded text-xs font-medium ${ok ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
      {ok ? 'Meets' : 'Below'}
    </span>
  );

  return (
    <div className="w-full max-w-5xl mx-auto p-4">
      {/* Property summary */}
      <div className="rounded-lg border border-neutral-200 bg-white shadow-sm">
        <div className="border-b border-neutral-200 p-4">
          <h2 className="text-lg font-semibold">Property</h2>
          <p className="text-sm text-neutral-600">{property.formattedAddress || 'Unknown address'}</p>
        </div>
        <div className="grid grid-cols-1 gap-4 p-4 sm:grid-cols-2 lg:grid-cols-3">
          {property.city && <Info label="City" value={property.city} />}
          {property.state && <Info label="State" value={property.state} />}
          {property.zipCode && <Info label="ZIP" value={property.zipCode} />}
          {property.propertyType && <Info label="Type" value={property.propertyType} />}
          {property.bedrooms != null && <Info label="Beds" value={property.bedrooms} />}
          {property.bathrooms != null && <Info label="Baths" value={property.bathrooms} />}
          {property.squareFootage != null && <Info label="Sq Ft" value={property.squareFootage} />}
          {fin.property_value != null && <Info label="Est. Value" value={`$${Number(fin.property_value).toLocaleString()}`} />}
        </div>
      </div>

      {/* Rent & Cap Rates */}
      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-base font-semibold">Rent estimates</h3>
          <ul className="space-y-2 text-sm">
            <li className="flex justify-between"><span>Low</span><span>${Number(rents.rent_low || 0).toLocaleString()}</span></li>
            <li className="flex justify-between"><span>Mid</span><span>${Number(rents.rent || 0).toLocaleString()}</span></li>
            <li className="flex justify-between"><span>High</span><span>${Number(rents.rent_high || 0).toLocaleString()}</span></li>
          </ul>
          {rents.source && (
            <p className="mt-2 text-xs text-neutral-500">Source: {rents.source}</p>
          )}
        </div>

        <div className="rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
          <div className="flex items-center justify-between">
            <h3 className="mb-3 text-base font-semibold">Cap rates</h3>
            {fin.calculation_mode && (
              <span className="text-xs text-neutral-500">Mode: {fin.calculation_mode}</span>
            )}
          </div>
          {caps.error ? (
            <p className="text-sm text-red-600">{caps.error}</p>
          ) : (
            <ul className="space-y-2 text-sm">
              <li className="flex items-center justify-between">
                <span>Low</span>
                <span className="flex items-center gap-2">{Number(caps.low || 0).toFixed(2)}% {fin.meets_threshold && <CapBadge ok={!!fin.meets_threshold.low} />}</span>
              </li>
              <li className="flex items-center justify-between">
                <span>Mid</span>
                <span className="flex items-center gap-2">{Number(caps.mid || 0).toFixed(2)}% {fin.meets_threshold && <CapBadge ok={!!fin.meets_threshold.mid} />}</span>
              </li>
              <li className="flex items-center justify-between">
                <span>High</span>
                <span className="flex items-center gap-2">{Number(caps.high || 0).toFixed(2)}% {fin.meets_threshold && <CapBadge ok={!!fin.meets_threshold.high} />}</span>
              </li>
            </ul>
          )}
          {fin.api_calls_remaining != null && (
            <p className="mt-2 text-xs text-neutral-500">API calls remaining (RentCast): {fin.api_calls_remaining}</p>
          )}
        </div>
      </div>

      {/* Recommendation */}
      {rec.decision && (
        <div className="mt-6 rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
          <h3 className="mb-2 text-base font-semibold">Recommendation</h3>
          <p className="text-sm"><span className="font-medium">{rec.decision}</span> — {rec.reason}</p>
        </div>
      )}

      {/* Expenses used (optional) */}
      {fin.expenses_used && (
        <div className="mt-6 rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-base font-semibold">Expense assumptions</h3>
          <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 md:grid-cols-3 text-sm">
            {Object.entries(fin.expenses_used).map(([k, v]) => (
              <div key={k} className="flex justify-between">
                <span className="capitalize">{k.replaceAll('_', ' ')}</span>
                <span>{(Number(v) * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Analysis */}
      {ai && (
        <div className="mt-6 rounded-lg border border-neutral-200 bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-base font-semibold">AI investment analysis</h3>
          <pre className="max-h-96 overflow-auto rounded bg-neutral-50 p-3 text-xs text-neutral-800">
{JSON.stringify(ai, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

const Info = ({ label, value }) => (
  <div className="rounded-md border border-neutral-200 bg-white p-3">
    <div className="text-xs uppercase tracking-wide text-neutral-500">{label}</div>
    <div className="text-sm font-medium text-neutral-900">{value}</div>
  </div>
);

export default AnalysisReportDisplay;
