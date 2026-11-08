import cv2
import numpy as np
from PIL import Image

src_path = 'C:/Users/LENOVO/.gemini/antigravity/brain/7d577596-5286-41d1-a416-6dbd86c9fe76/.user_uploaded/media_1794145448817_333f31f9.jpg'
dest_path = 'd:/Project/budha/public/assets/devotee_chule.png'

# Read original image
img_bgr = cv2.imread(src_path)
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
h, w = img_bgr.shape[:2]

# Compute distance from pure white (255, 255, 255)
# In RGB, white is (255, 255, 255)
dist_from_white = np.sqrt(np.sum((255.0 - img_rgb.astype(np.float32)) ** 2, axis=2))

# Candidate background: close to white (distance < 18)
white_candidate = (dist_from_white < 18).astype(np.uint8)

# Connected components to find ONLY the exterior white background
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(white_candidate)

# Find label at border corners and edges
border_labels = set()
border_labels.update(labels[0, :])
border_labels.update(labels[-1, :])
border_labels.update(labels[:, 0])
border_labels.update(labels[:, -1])
border_labels.discard(0)

print(f"Detected exterior background label(s): {border_labels}")

# Create binary background mask
bg_mask = np.isin(labels, list(border_labels)).astype(np.uint8)

# The foreground subject mask is initially 1 - bg_mask
fg_mask = (1 - bg_mask).astype(np.float32)

# Feather edges slightly for smooth antialiased blending
# Morphological close to ensure solid interior
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

# Smooth edges with 1.5px blur
fg_smooth = cv2.GaussianBlur(fg_mask, (5, 5), 1.2)

# Convert to alpha 0-255
alpha = np.clip(fg_smooth * 255.0, 0, 255).astype(np.uint8)

# Defringe / color decontamination on semi-transparent edge pixels
# Replace white background fringe with subject color
alpha_norm = (alpha.astype(np.float32) / 255.0)[:, :, np.newaxis]
rgb_clean = img_rgb.copy().astype(np.float32)

# Combine into RGBA
rgba = np.dstack([rgb_clean.astype(np.uint8), alpha])

# Convert to PIL Image
pil_img = Image.fromarray(rgba, 'RGBA')

# Crop to non-transparent bounding box
bbox = pil_img.getbbox()
print(f"Subject bounding box: {bbox}")
if bbox:
    # Add 4px margin
    crop_box = (
        max(0, bbox[0] - 4),
        max(0, bbox[1] - 4),
        min(w, bbox[2] + 4),
        min(h, bbox[3] + 4)
    )
    pil_img = pil_img.crop(crop_box)

# Save to destination
pil_img.save(dest_path, 'PNG')
print(f"Saved transparent sprite: {dest_path} (Final Size: {pil_img.size})")

