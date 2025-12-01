import { apiClient } from '../config/api.js';

export async function getProperties({
  skip = 0,
  limit = 25,
  city,
  state,
  propertyType,
  minPrice,
  maxPrice,
  bedrooms
} = {}) {
  const params = new URLSearchParams();

  params.append('skip', skip.toString());
  params.append('limit', limit.toString());

  if (city) params.append('city', city);
  if (state) params.append('state', state);
  if (propertyType) params.append('property_type', propertyType);
  if (minPrice) params.append('min_price', minPrice.toString());
  if (maxPrice) params.append('max_price', maxPrice.toString());
  if (bedrooms) params.append('bedrooms', bedrooms.toString());

  const response = await apiClient.get(`/api/properties?${params.toString()}`);
  return response.data;
}

export async function getProperty(propertyId) {
  const response = await apiClient.get(`/api/properties/${propertyId}`);
  return response.data;
}

export async function createProperty(propertyData) {
  const response = await apiClient.post('/api/properties', propertyData);
  return response.data;
}

export async function updateProperty(propertyId, propertyData) {
  const response = await apiClient.patch(`/api/properties/${propertyId}`, propertyData);
  return response.data;
}

export async function deleteProperty(propertyId) {
  const response = await apiClient.delete(`/api/properties/${propertyId}`);
  return response.data;
}

export async function analyzeProperty(propertyId, analysisData) {
  const response = await apiClient.post(`/api/properties/${propertyId}/analysis`, analysisData);
  return response.data;
}

export async function analyzeByAddress({ street, city, state, zip, overrides, monthlyRent } = {}) {
  const payload = { street, city, state, zip };
  if (overrides && Object.keys(overrides).length > 0) {
    payload.overrides = overrides;
  }
  if (monthlyRent !== undefined && monthlyRent !== null && monthlyRent !== '') {
    const num = Number(monthlyRent);
    if (!Number.isNaN(num)) payload.monthlyRent = num;
  }
  const response = await apiClient.post(`/api/properties/analyze-by-address`, payload);
  return response.data;
}

export async function searchPropertiesByAddress(address, limit = 8) {
  const params = new URLSearchParams();
  params.append('address', address);
  params.append('limit', limit.toString());
  const response = await apiClient.get(`/api/properties/search?${params.toString()}`);
  return response.data;
}

// Keep the old object export for backward compatibility if needed
export const propertyService = {
  getProperties,
  getProperty,
  createProperty,
  updateProperty,
  deleteProperty,
  analyzeProperty,
  analyzeByAddress,
  searchPropertiesByAddress
};