const DEFAULT_IMAGES = [
  '/assets/images/defaults/property-1.jpg',
  '/assets/images/defaults/property-2.jpg',
  '/assets/images/defaults/property-3.jpg',
  '/assets/images/defaults/property-4.jpg',
  '/assets/images/defaults/property-5.jpg',
];

export const getPropertyImage = (property) => {
  if (property.image || property.imageUrl) {
    return property.image || property.imageUrl;
  }

  const index = property.id % DEFAULT_IMAGES.length;
  return DEFAULT_IMAGES[index];
};