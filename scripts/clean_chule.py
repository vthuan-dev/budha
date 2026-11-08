from PIL import Image
import numpy as np

im = Image.open("public/assets/devotee_chule.png").convert("RGBA")
w, h = im.size
arr = np.array(im)

# Hair starts around y=42 (where the black bun is)
# Anything above y=42 should be transparent
arr[0:42, :, 3] = 0

# Clean red carpet halo edge if any
# Red halo: pixels with alpha > 0 where R > 150 and G < 90 and B < 90
for y in range(h):
    for x in range(w):
        if arr[y, x, 3] > 0:
            r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
            if r > 140 and g < 70 and b < 70:
                arr[y, x, 3] = 0

cleaned = Image.fromarray(arr, "RGBA")
bbox = cleaned.getbbox()
if bbox:
    cleaned = cleaned.crop(bbox)
cleaned.save("public/assets/devotee_chule.png", "PNG")
print("Cleaned devotee_chule.png successfully!")
