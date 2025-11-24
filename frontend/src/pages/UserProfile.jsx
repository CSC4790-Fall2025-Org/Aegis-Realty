import { useState } from 'react';
import { FiEdit2, FiSave, FiX, FiHeart, FiMail, FiUser } from 'react-icons/fi';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../contexts/ToastContext';
import {
  useUpdateUser,
  useFavoriteProperties,
  useRemoveFavorite
} from '../hooks/useUserQueries';
import { getPropertyImage } from '../utils/imageHelper';

const UserProfile = () => {
  const { currentUser, updateUserData } = useAuth();
  const toast = useToast();
  const [displayName, setDisplayName] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  const userData = currentUser;

  const { data: favoriteProperties = [], isLoading: favoritesLoading } = useFavoriteProperties(userData?.id);
  const updateUserMutation = useUpdateUser();
  const removeFavoriteMutation = useRemoveFavorite();

  const handleUpdateProfile = async (e) => {
    e.preventDefault();

    if (!userData?.id) {
      toast.error('Profile not found');
      return;
    }

    try {
      await updateUserMutation.mutateAsync({
        id: userData.id,
        userData: { display_name: displayName }
      });
      updateUserData();
      toast.success('Profile updated successfully');
      setIsEditing(false);
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };

  const handleRemoveFavorite = async (propertyId) => {
    if (!userData?.id) {
      toast.error('Profile not found');
      return;
    }

    try {
      await removeFavoriteMutation.mutateAsync({
        userId: userData.id,
        propertyId
      });
      updateUserData();
      toast.success('Property removed from favorites');
    } catch (error) {
      toast.error('Failed to remove favorite');
    }
  };

  const startEditing = () => {
    setDisplayName(userData?.display_name ?? currentUser?.firebaseUser?.displayName ?? '');
    setIsEditing(true);
  };

  if (!userData?.id) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="bg-background rounded-lg shadow-lg p-8 text-center">
          <FiUser size={48} className="text-text opacity-30 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-text mb-2">Profile Not Found</h2>
          <p className="text-text opacity-70">Please contact support to set up your account.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <h1 className="text-4xl font-bold text-text mb-8">My Profile</h1>

      <div className="bg-background rounded-lg shadow-lg p-8 mb-8">
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className="bg-primary rounded-full p-4">
              <FiUser size={32} className="text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-text">
                {userData.display_name || currentUser?.firebaseUser?.displayName || 'User'}
              </h2>
              <p className="text-text opacity-70">{userData.email || currentUser?.firebaseUser?.email || 'No email'}</p>
            </div>
          </div>
          {!isEditing && (
            <button
              onClick={startEditing}
              className="flex items-center space-x-2 bg-primary text-white px-4 py-2 rounded-md hover:bg-opacity-90 transition-colors cursor-pointer"
            >
              <FiEdit2 size={18} />
              <span>Edit Profile</span>
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <label className="flex items-center space-x-2 text-text font-medium mb-2">
                <FiMail size={18} />
                <span>Email Address</span>
              </label>
              <p className="text-text bg-secondary px-4 py-3 rounded-md">{userData.email || 'Not available'}</p>
            </div>

            <div>
              <label className="flex items-center space-x-2 text-text font-medium mb-2">
                <FiUser size={18} />
                <span>Display Name</span>
              </label>
              {isEditing ? (
                <form onSubmit={handleUpdateProfile} className="space-y-3">
                  <input
                    type="text"
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                    placeholder="Enter display name"
                    className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                  <div className="flex space-x-2">
                    <button
                      type="submit"
                      disabled={updateUserMutation.isLoading}
                      className="flex items-center space-x-2 bg-primary text-white px-4 py-2 rounded-md hover:bg-secondary/80 disabled:opacity-50 cursor-pointer"
                    >
                      <FiSave size={18} />
                      <span>{updateUserMutation.isLoading ? 'Saving...' : 'Save'}</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => setIsEditing(false)}
                      className="flex items-center space-x-2 bg-gray-400 text-white px-2 py-2 rounded-md hover:bg-secondary/80 cursor-pointer"
                    >
                      <FiX size={18} />
                      <span>Cancel</span>
                    </button>
                  </div>
                </form>
              ) : (
                <p className="text-text bg-secondary px-4 py-3 rounded-md">
                  {userData.display_name || currentUser?.firebaseUser?.displayName || 'Not set'}
                </p>
              )}
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="flex items-center space-x-2 text-text font-medium mb-2">
                <FiHeart size={18} />
                <span>Favorite Properties</span>
              </label>
              <p className="text-text bg-secondary px-4 py-3 rounded-md">
                {favoriteProperties.length} {favoriteProperties.length === 1 ? 'property' : 'properties'}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-background rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-text mb-6 flex items-center space-x-2">
          <FiHeart size={24} />
          <span>Favorite Properties</span>
        </h2>

        {favoritesLoading ? (
          <div className="text-center text-text py-8">Loading favorites...</div>
        ) : favoriteProperties.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {favoriteProperties.map((property) => (
              <div key={property.id} className="bg-secondary rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow">
                <img
                  src={getPropertyImage(property)}
                  alt="property"
                  className="w-full h-48 object-cover"
                />
                <div className="p-4">
                  <h3 className="text-text font-semibold mb-2 truncate">
                    {property.formattedAddress}
                  </h3>
                  <p className="text-text text-lg font-bold mb-4">
                    ${property.lastSalePrice?.toLocaleString() || 'N/A'}
                  </p>
                  <button
                    onClick={() => handleRemoveFavorite(property.id)}
                    disabled={removeFavoriteMutation.isLoading}
                    className="w-full flex items-center justify-center space-x-2 bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 disabled:opacity-50 transition-colors cursor-pointer"
                  >
                    <FiX size={18} />
                    <span>Remove</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <FiHeart size={48} className="text-text opacity-30 mx-auto mb-4" />
            <p className="text-text text-lg">No favorite properties yet</p>
            <p className="text-text opacity-70 mt-2">Browse properties to add them to your favorites!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserProfile;