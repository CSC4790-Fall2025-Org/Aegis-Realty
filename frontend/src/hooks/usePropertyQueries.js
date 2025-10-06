import { useInfiniteQuery, useQuery } from '@tanstack/react-query';
import { getProperties, getProperty } from '../services/propertyServices.js';

export const useInfiniteProperties = (filters = {}) => {
  return useInfiniteQuery({
    queryKey: ['properties', 'infinite', filters],
    queryFn: ({ pageParam = 0 }) => {
      return getProperties({
        skip: pageParam,
        limit: 25,
        ...filters
      });
    },
    getNextPageParam: (lastPage, allPages) => {
      if (lastPage.length < 25) {
        return undefined;
      }
      return allPages.length * 25;
    },
    staleTime: 5 * 60 * 1000,
    cacheTime: 10 * 60 * 1000,
  });
};

export const useProperty = (propertyId) => {
  return useQuery({
    queryKey: ['properties', propertyId],
    queryFn: () => getProperty(propertyId),
    enabled: !!propertyId,
    staleTime: 5 * 60 * 1000,
    cacheTime: 10 * 60 * 1000,
  });
};

export const useProperties = (filters = {}) => {
  return useQuery({
    queryKey: ['properties', filters],
    queryFn: () => getProperties(filters),
    staleTime: 5 * 60 * 1000,
    cacheTime: 10 * 60 * 1000,
  });
};