from PIL import Image, ImageFilter, ImageDraw
import numpy as np

# Load wide stage
im = Image.open(r"C:\Users\LENOVO\.gemini\antigravity\brain\7d577596-5286-41d1-a416-6dbd86c9fe76\thien_canh_wide_raw_1794066629928.jpg").convert("RGB")
w, h = im.size
print("Size:", w, h)

# Let's inspect wooden floor sample from bottom corners or aisle
# Bottom wooden floor: around x=10..120, y=1800..1920
# or around carpet edges
