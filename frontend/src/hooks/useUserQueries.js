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
      queryClient.invalidateQueries({ queryKey: ['user', data.id] });
      queryClient.invalidateQueries({ queryKey: ['user', 'firebase', data.firebase_id] });
      queryClient.invalidateQueries({ queryKey: ['users'] });


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
      queryClient.invalidateQueries({ queryKey: ['users'] });
      queryClient.removeQueries({ queryKey: ['user', variables] });

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

export function useAddFavorite(options = {}) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ userId, propertyId }) => userServices.addFavoriteProperty(userId, propertyId),
    onMutate: async ({ propertyId }) => {
      await queryClient.cancelQueries({ queryKey: ['user'] });

      queryClient.setQueriesData({ queryKey: ['user'] }, (old) => {
        if (!old) return old;
        return {
          ...old,
          favorite_properties: [...(old.favorite_properties || []), propertyId]
        };
      });
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['user'] });
      options.onSuccess?.(data);
    },
    ...options,
  });
}

export function useRemoveFavorite(options = {}) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({userId, propertyId}) => userServices.removeFavoriteProperty(userId, propertyId),
    onMutate: async ({ propertyId }) => {
      await queryClient.cancelQueries({ queryKey: ['user'] });

      queryClient.setQueriesData({ queryKey: ['user'] }, (old) => {
        if (!old) return old;
        return {
          ...old,
          favorite_properties: (old.favorite_properties || []).filter(id => id !== propertyId)
        };
      });
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['user'] });
      options.onSuccess?.(data);
    },
    ...options,
  });
}

export function useFavoriteProperties(userId, options = {}) {
  return useQuery({
    queryKey: ['user', userId, 'favorites'],
    queryFn: () => userServices.getFavoriteProperties(userId),
    enabled: !!userId,
    ...options,
  });
}