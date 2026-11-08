from PIL import Image, ImageFilter
import numpy as np

im = Image.open("public/assets/chule_crop_raw.png").convert("RGBA")
w, h = im.size
arr = np.array(im, dtype=np.float32)

r = arr[:, :, 0]
g = arr[:, :, 1]
b = arr[:, :, 2]

# The white ao dai has high brightness (r, g, b all high and close to each other)
# The red carpet has high r, but low g and low b: (r > 100, g < 60, b < 60)
# Dark hair has low r, g, b around the top center
# Let's compute a mask:
# 1. White ao dai: brightness = (r + g + b) / 3 > 140, or (g > 100 and b > 100)
# 2. Dark hair: x between 150..250, y between 30..150, brightness < 90
# 3. Hands / neck: flesh tones

mask = np.zeros((h, w), dtype=np.uint8)

for y in range(h):
    for x in range(w):
        # Discard outer margins
        dist_from_center = abs(x - 200)
        # Symmetrical trapezoid boundary for sitting figure
        # At y=30 (head): max width ~ 45
        # At y=400 (waist): max width ~ 85
        # At y=650 (kneeling hem): max width ~ 140
        max_dist = 30 + (y / h) * 125
        if dist_from_center > max_dist:
            continue
        
        red = r[y, x]
        green = g[y, x]
        blue = b[y, x]
        bright = (red + green + blue) / 3.0
        
        # Head area (y < 140)
        if y < 140:
            if dist_from_center < 42:
                # Dark hair or flower pin or neck
                if bright < 110 or (green > 120 and blue > 120):
                    mask[y, x] = 255
            continue
        
        # Body / Ao dai area (y >= 140)
        # Red carpet has: red > green + 45 and red > blue + 45
        is_red_carpet = (red > green + 38) and (red > blue + 38) and (green < 110)
        if not is_red_carpet and bright > 90:
            mask[y, x] = 255

# Smooth the mask
mask_im = Image.fromarray(mask, mode="L")
mask_im = mask_im.filter(ImageFilter.GaussianBlur(1.2))

# Apply mask to image
im.putalpha(mask_im)

# Crop to non-empty bounding box
bbox = im.getbbox()
if bbox:
    im_cropped = im.crop(bbox)
    im_cropped.save("public/assets/devotee_chule.png", "PNG")
    print("Saved devotee_chule.png, size:", im_cropped.size)
else:
    print("Empty mask")
