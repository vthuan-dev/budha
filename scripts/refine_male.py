from PIL import Image, ImageDraw, ImageFilter
import numpy as np

base = Image.open("public/assets/devotee.png").convert("RGBA")
w, h = base.size

# Clone base
male = base.copy()
# We want to replace the bun (y=7..28) with natural rounded hair.
# In the original, the head contour without bun starts at y=28, width around x=48..90
# Let's erase y < 27
arr = np.array(male)
arr[0:27, :, 3] = 0

# Sample hair color from y=35, x=69:
hair_sample = arr[35, 69, :3] # typically dark brown/black

# Create a smooth head crown:
# Draw a soft rounded dark haircut with gradient
crown = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(crown)

# Head top arc: x from 48 to 90 (center 69, width 42), y from 22 to 50
d.ellipse([48, 20, 90, 52], fill=(28, 22, 20, 255))
# Inner hair tone
d.ellipse([51, 23, 87, 49], fill=(42, 32, 28, 255))
# Shading highlight
d.ellipse([56, 25, 82, 42], fill=(65, 50, 42, 200))
# Rim light on the edge
d.arc([47, 19, 91, 53], start=185, end=355, fill=(255, 200, 110, 230), width=2)

crown = crown.filter(ImageFilter.GaussianBlur(0.7))

# Merge
male_img = Image.fromarray(arr, "RGBA")
final_male = Image.alpha_composite(male_img, crown)
final_male.save("public/assets/devotee_male.png", "PNG")
print("Refined devotee_male.png successfully!")
