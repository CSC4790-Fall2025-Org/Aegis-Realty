const DEFAULT_IMAGES = [
  'src/assets/images/defaults/property-1.jpg',
  'src/assets/images/defaults/property-2.jpg',
  'src/assets/images/defaults/property-3.jpg',
  'src/assets/images/defaults/property-4.jpg',
  'src/assets/images/defaults/property-5.jpg',
];

export const getPropertyImage = (property) => {
  if (property.image || property.imageUrl) {
    return property.image || property.imageUrl;
  }

  const index = property.id % DEFAULT_IMAGES.length;
  return DEFAULT_IMAGES[index];
};