import img1 from '../assets/images/defaults/property-1.jpg';
import img2 from '../assets/images/defaults/property-2.jpg';
import img3 from '../assets/images/defaults/property-3.jpg';
import img4 from '../assets/images/defaults/property-4.jpg';
import img5 from '../assets/images/defaults/property-5.jpg';

const DEFAULT_IMAGES = [img1, img2, img3, img4, img5];

export const getPropertyImage = (property = {}) => {
  // Common fields that may carry image URLs
  const candidates = [
    property.image,
    property.imageUrl,
    property.photoUrl,
    Array.isArray(property.photos) ? property.photos[0] : undefined,
    Array.isArray(property.images) ? property.images[0] : undefined,
  ].filter(Boolean);

  if (candidates.length > 0) {
    return candidates[0];
  }

  // Deterministic default image based on id/address hash
  const key = (property.id ?? 0).toString() + (property.formattedAddress ?? '');
  let hash = 0;
  for (let i = 0; i < key.length; i++) {
    hash = (hash * 31 + key.charCodeAt(i)) >>> 0;
  }
  const index = hash % DEFAULT_IMAGES.length;
  return DEFAULT_IMAGES[index];
};