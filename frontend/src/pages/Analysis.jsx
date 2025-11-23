import { useState } from 'react';
import { analyzeByAddress } from '../services/propertyServices.js';
import Spinner from '../components/Spinner.jsx';

const Field = ({ label, value, onChange, placeholder, name }) => (
  <div className="flex flex-col gap-1">
    <label className="text-sm text-text/80" htmlFor={name}>{label}</label>
    <input
      id={name}
      name={name}
      type="text"
      className="border rounded px-3 py-2 bg-background text-text focus:outline-none focus:ring-2 focus:ring-primary"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      required
    />
  </div>
);

const ResultCard = ({ result }) => {
  if (!result) return null;
  const tone = result.recommendation === 'Worth investing' ? 'text-green-600' : result.recommendation === 'Maybe' ? 'text-amber-600' : 'text-red-600';

  const copyReport = () => {
    if (result.report) {
      navigator.clipboard.writeText(result.report).catch(() => {});
    }
  };

  return (
    <div className="mt-6 border rounded-lg p-4 bg-white dark:bg-secondary shadow">
      <h3 className="text-lg font-semibold mb-2">Analysis Result</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div>
          <div className="text-sm text-text/70">Cap rate</div>
          <div className="text-xl font-bold">{result.cap_rate_percent}%</div>
        </div>
        <div>
          <div className="text-sm text-text/70">Recommendation</div>
          <div className={`text-xl font-bold ${tone}`}>{result.recommendation}</div>
        </div>
      </div>
      <div className="mt-3 text-text/90">{result.explanation}</div>
      {result.property_address && (
        <div className="mt-2 text-sm text-text/70">Property: {result.property_address}</div>
      )}
      {result.details && (
        <details className="mt-4">
          <summary className="cursor-pointer text-sm text-text/70">Details</summary>
          <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
            <div>Value: ${result.details.value}</div>
            <div>Monthly Rent: ${result.details.monthly_rent}</div>
            <div>Annual Rent: ${result.details.annual_rent}</div>
            <div>Annual Expenses: ${result.details.annual_expenses}</div>
            <div>NOI: ${result.details.noi}</div>
          </div>
        </details>
      )}
      {result.report && (
        <details className="mt-4">
          <summary className="cursor-pointer text-sm text-text/70">Full Narrative Report</summary>
          <div className="mt-3 whitespace-pre-wrap text-sm leading-relaxed font-mono bg-background/40 dark:bg-background/20 p-3 rounded border">
            {result.report}
          </div>
          <button
            type="button"
            onClick={copyReport}
            className="mt-2 text-xs px-3 py-1 rounded bg-primary text-white hover:bg-opacity-90"
          >Copy Report</button>
        </details>
      )}
    </div>
  );
};

const Analysis = () => {
  const [street, setStreet] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [zip, setZip] = useState('');
  const [monthlyRent, setMonthlyRent] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  // Optional overrides state (rates are fractions; amounts are dollars)
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [overrides, setOverrides] = useState({
    property_management_rate: '',
    maintenance_repairs_rate: '',
    vacancy_allowance_rate: '',
    insurance_rate: '',
    property_tax_rate: '',
    utilities_rate: '',
    hoa_monthly: '',
    hoa_annual: '',
    taxes_annual: ''
  });

  const setOverride = (key) => (val) => setOverrides((prev) => ({ ...prev, [key]: val }));

  const buildOverrides = () => {
    const o = {};
    const numberKeys = [
      'property_management_rate',
      'maintenance_repairs_rate',
      'vacancy_allowance_rate',
      'insurance_rate',
      'property_tax_rate',
      'utilities_rate',
      'hoa_monthly',
      'hoa_annual',
      'taxes_annual',
    ];
    numberKeys.forEach((k) => {
      const v = overrides[k];
      if (v !== '' && v !== null && v !== undefined) {
        const num = Number(v);
        if (!Number.isNaN(num)) o[k] = num;
      }
    });
    return o;
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);

    if (!street || !city || !state || !zip) {
      setError('Please fill out all fields.');
      return;
    }

    try {
      setLoading(true);
  const o = buildOverrides();
  const data = await analyzeByAddress({ street, city, state, zip, overrides: o, monthlyRent });
      setResult(data);
    } catch (err) {
      const msg = err?.response?.data?.detail || 'An error occurred during analysis.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <h1 className="text-2xl font-bold mb-4">Analyze Property Investment</h1>
      <form onSubmit={onSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-white dark:bg-secondary p-4 rounded shadow">
        <Field label="Street" name="street" value={street} onChange={setStreet} placeholder="123 Main St" />
        <Field label="City" name="city" value={city} onChange={setCity} placeholder="Anytown" />
        <Field label="State" name="state" value={state} onChange={setState} placeholder="CA" />
        <Field label="Zip Code" name="zip" value={zip} onChange={setZip} placeholder="90210" />
        <div className="flex flex-col gap-1">
          <label className="text-sm text-text/80" htmlFor="monthlyRent">Monthly Rent (override, optional)</label>
          <input
            id="monthlyRent"
            name="monthlyRent"
            type="number"
            step="0.01"
            className="border rounded px-3 py-2 bg-background text-text focus:outline-none focus:ring-2 focus:ring-primary"
            value={monthlyRent}
            onChange={(e) => setMonthlyRent(e.target.value)}
            placeholder="e.g., 2450"
          />
        </div>

        <div className="sm:col-span-2">
          <button
            type="button"
            onClick={() => setShowAdvanced((s) => !s)}
            className="text-sm text-primary underline"
          >{showAdvanced ? 'Hide' : 'Show'} Advanced Overrides</button>
        </div>

        {showAdvanced && (
          <div className="sm:col-span-2 border rounded p-3 space-y-3">
            <div className="text-sm text-text/80">Rates are fractions (e.g., 0.10 = 10%). Amounts are in dollars.</div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label className="text-xs text-text/70" htmlFor="pm_rate">Property Mgmt Rate</label>
                <input id="pm_rate" type="number" step="0.001" className="w-full border rounded px-2 py-1 bg-background text-text" value={overrides.property_management_rate} onChange={(e)=>setOverride('property_management_rate')(e.target.value)} placeholder="0.10" />
              </div>
              <div>
                <label className="text-xs text-text/70" htmlFor="maint_rate">Maintenance Rate</label>
                <input id="maint_rate" type="number" step="0.001" className="w-full border rounded px-2 py-1 bg-background text-text" value={overrides.maintenance_repairs_rate} onChange={(e)=>setOverride('maintenance_repairs_rate')(e.target.value)} placeholder="0.08" />
              </div>
              <div>
                <label className="text-xs text-text/70" htmlFor="vacancy_rate">Vacancy Rate</label>
                <input id="vacancy_rate" type="number" step="0.001" className="w-full border rounded px-2 py-1 bg-background text-text" value={overrides.vacancy_allowance_rate} onChange={(e)=>setOverride('vacancy_allowance_rate')(e.target.value)} placeholder="0.06" />
              </div>
              <div>
                <label className="text-xs text-text/70" htmlFor="ins_rate">Insurance Rate (value)</label>
                <input id="ins_rate" type="number" step="0.0001" className="w-full border rounded px-2 py-1 bg-background text-text" value={overrides.insurance_rate} onChange={(e)=>setOverride('insurance_rate')(e.target.value)} placeholder="0.007" />
              </div>
              <div>
                <label className="text-xs text-text/70" htmlFor="tax_rate">Property Tax Rate (fallback)</label>
                <input id="tax_rate" type="number" step="0.0001" className="w-full border rounded px-2 py-1 bg-background text-text" value={overrides.property_tax_rate} onChange={(e)=>setOverride('property_tax_rate')(e.target.value)} placeholder="0.013" />
              </div>
              <div>
                <label className="text-xs text-text/70" htmlFor="util_rate">Utilities Rate</label>
                <input id="util_rate" type="number" step="0.001" className="w-full border rounded px-2 py-1 bg-background text-text" value={overrides.utilities_rate} onChange={(e)=>setOverride('utilities_rate')(e.target.value)} placeholder="0.00" />
              </div>
              <div>
                <label className="text-xs text-text/70" htmlFor="hoa_mo">HOA Monthly ($)</label>
                <input id="hoa_mo" type="number" step="0.01" className="w-full border rounded px-2 py-1 bg-background text-text" value={overrides.hoa_monthly} onChange={(e)=>setOverride('hoa_monthly')(e.target.value)} placeholder="150" />
              </div>
              <div>
                <label className="text-xs text-text/70" htmlFor="hoa_an">HOA Annual ($)</label>
                <input id="hoa_an" type="number" step="0.01" className="w-full border rounded px-2 py-1 bg-background text-text" value={overrides.hoa_annual} onChange={(e)=>setOverride('hoa_annual')(e.target.value)} placeholder="1800" />
              </div>
              <div>
                <label className="text-xs text-text/70" htmlFor="tax_an">Taxes Annual ($)</label>
                <input id="tax_an" type="number" step="0.01" className="w-full border rounded px-2 py-1 bg-background text-text" value={overrides.taxes_annual} onChange={(e)=>setOverride('taxes_annual')(e.target.value)} placeholder="3500" />
              </div>
            </div>
          </div>
        )}

        <div className="sm:col-span-2 flex items-center gap-3 mt-2">
          <button
            type="submit"
            className="bg-primary text-white px-4 py-2 rounded hover:bg-opacity-90 disabled:opacity-60"
            disabled={loading}
          >
            {loading ? <span className="inline-flex items-center gap-2"><Spinner size={18}/> Analyzing...</span> : 'Analysis'}
          </button>
          {error && <div className="text-red-600 text-sm">{error}</div>}
        </div>
      </form>

      <ResultCard result={result} />
    </div>
  );
};

export default Analysis;
