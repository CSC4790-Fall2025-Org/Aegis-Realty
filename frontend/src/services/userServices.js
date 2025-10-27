import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export async function createUser(userData) {
  const response = await axios.post(`${BASE_URL}/api/users`, userData);
  return response.data;
}

export async function getUsers(skip = 0, limit = 100) {
  const response = await axios.get(`${BASE_URL}/api/users?skip=${skip}&limit=${limit}`);
  return response.data;
}

export async function getUserById(id) {
  const response = await axios.get(`${BASE_URL}/api/users/${id}`);
  return response.data;
}

export async function getUserByFirebaseId(firebaseId) {
  const response = await axios.get(`${BASE_URL}/api/users/firebase/${firebaseId}`);
  return response.data;
}

export async function updateUser(id, userData) {
  const response = await axios.patch(`${BASE_URL}/api/users/${id}`, userData);
  return response.data;
}

export async function deleteUser(id) {
  const response = await axios.delete(`${BASE_URL}/api/users/${id}`);
  return response.data;
}