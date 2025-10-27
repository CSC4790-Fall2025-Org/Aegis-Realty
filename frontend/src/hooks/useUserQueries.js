import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as userServices from '../services/userServices';

export function useUsers(options = {}) {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => userServices.getUsers(),
    ...options,
  });
}

export function useUserById(id, options = {}) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: () => userServices.getUserById(id),
    enabled: !!id,
    ...options,
  });
}

export function useUserByFirebaseId(firebaseId, options = {}) {
  return useQuery({
    queryKey: ['user', 'firebase', firebaseId],
    queryFn: () => userServices.getUserByFirebaseId(firebaseId),
    enabled: !!firebaseId,
    ...options,
  });
}

export function useCreateUser(options = {}) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (userData) => userServices.createUser(userData),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      queryClient.setQueryData(['user', data.id], data);
      queryClient.setQueryData(['user', 'firebase', data.firebase_id], data);

      if (options.onSuccess) {
        options.onSuccess(data);
      }
    },
    ...options,
  });
}

export function useUpdateUser(options = {}) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, userData }) => userServices.updateUser(id, userData),
    onSuccess: (data) => {
      // Invalidate relevant queries
      queryClient.invalidateQueries({ queryKey: ['user', data.id] });
      queryClient.invalidateQueries({ queryKey: ['user', 'firebase', data.firebase_id] });
      queryClient.invalidateQueries({ queryKey: ['users'] });

      // If the user belongs to a company, invalidate company users
      if (data.company_id) {
        queryClient.invalidateQueries({ queryKey: ['company', data.company_id, 'users'] });
      }

      if (options.onSuccess) {
        options.onSuccess(data);
      }
    },
    ...options,
  });
}

export function useDeleteUser(options = {}) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id) => userServices.deleteUser(id),
    onSuccess: (data, variables) => {
      // Variables is the id we passed to the mutation
      queryClient.invalidateQueries({ queryKey: ['users'] });
      queryClient.removeQueries({ queryKey: ['user', variables] });

      // If we know the firebase_id and company_id, we could invalidate those too
      if (data.firebase_id) {
        queryClient.removeQueries({ queryKey: ['user', 'firebase', data.firebase_id] });
      }

      if (data.company_id) {
        queryClient.invalidateQueries({ queryKey: ['company', data.company_id, 'users'] });
      }

      if (options.onSuccess) {
        options.onSuccess(data);
      }
    },
    ...options,
  });
}