import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../contexts/ToastContext';
import { useUserById } from '../hooks/useUserQueries.js'
import { getPropertyImage } from '../utils/imageHelper';

const UserProfile = () => {
  const { currentUser } = useAuth();
  const toast = useToast();
  const [displayName, setDisplayName] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [favoriteProperties, setFavoriteProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const [favIds, userRes] = await Promise.all([
        api.get('/favorites/'),
        api.get('/users/me')
      ]);

      setDisplayName(userRes.data.display_name || '');

      if (favIds.data.length > 0) {
        const propsRes = await api.get('/properties/', {
          params: { ids: favIds.data.join(',') }
        });
        setFavoriteProperties(propsRes.data);
      }
    } catch (error) {
      toast.error('Failed to load profile data');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      await api.put('/users/me', { display_name: displayName });
      toast.success('Profile updated successfully');
      setIsEditing(false);
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };

  if (loading) return <div className="container mx-auto px-4 py-8">Loading...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-text mb-8">User Profile</h1>

      <div className="bg-background rounded-lg shadow-md p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-text font-medium mb-2">Email</label>
            <p className="text-text">{currentUser?.email}</p>
          </div>

          <div>
            <label className="block text-text font-medium mb-2">Display Name</label>
            {isEditing ? (
              <form onSubmit={handleUpdateProfile} className="flex gap-2">
                <input
                  type="text"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  className="flex-1 px-3 py-2 border rounded-md"
                />
                <button type="submit" className="bg-primary text-white px-4 py-2 rounded-md">
                  Save
                </button>
                <button
                  type="button"
                  onClick={() => setIsEditing(false)}
                  className="bg-gray-400 text-white px-4 py-2 rounded-md"
                >
                  Cancel
                </button>
              </form>
            ) : (
              <div className="flex items-center gap-2">
                <p className="text-text">{displayName || 'Not set'}</p>
                <button
                  onClick={() => setIsEditing(true)}
                  className="text-primary hover:underline"
                >
                  Edit
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <h2 className="text-2xl font-bold text-text mb-4">Favorite Properties</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {favoriteProperties.map((property) => (
          <div key={property.id} className="bg-background rounded-lg shadow-md overflow-hidden">
            <img src={getPropertyImage(property)} alt="property" className="w-full h-48 object-cover" />
            <div className="p-4">
              <h3 className="text-text font-semibold">{property.formattedAddress}</h3>
              <p className="text-text">${property.lastSalePrice?.toLocaleString()}</p>
            </div>
          </div>
        ))}
        {favoriteProperties.length === 0 && (
          <p className="text-text col-span-full">No favorite properties yet.</p>
        )}
      </div>
    </div>
  );
};

export default UserProfile;
