from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

# 1. Create devotee_female.png from devotee.png with delicate lotus hairpin
im_fem = Image.open("public/assets/devotee.png").convert("RGBA")
w_f, h_f = im_fem.size

# Draw a delicate golden/pink lotus flower pin on the bun
draw_fem = ImageDraw.Draw(im_fem)
# Bun is around x=69, y=24
pin_x, pin_y = 78, 26
draw_fem.ellipse([pin_x-4, pin_y-4, pin_x+4, pin_y+4], fill=(255, 230, 180, 240))
draw_fem.ellipse([pin_x-2, pin_y-2, pin_x+2, pin_y+2], fill=(255, 140, 180, 255))
im_fem.save("public/assets/devotee_female.png", "PNG")
print("Saved devotee_female.png")

# 2. Create devotee_male.png from devotee.png:
# Male has short neat hair (remove the high bun y=7..28 and round the head)
im_male = Image.open("public/assets/devotee.png").convert("RGBA")
# Bun is y=7 to y=27, x=54 to x=86
# Replace bun area with transparent
arr = np.array(im_male)
# Find alpha
for y in range(0, 30):
    for x in range(w_f):
        arr[y, x, 3] = 0

# Round the head at y=28..45
im_no_bun = Image.fromarray(arr, "RGBA")
# Draw rounded short dark hair on top of head
draw_male = ImageDraw.Draw(im_no_bun)
# Head top curves around x=69, y=36, radius=19
draw_male.ellipse([50, 22, 88, 48], fill=(32, 24, 22, 255))
# Add soft warm rim light on head contour
draw_male.arc([49, 21, 89, 47], start=180, end=360, fill=(255, 200, 100, 220), width=2)

im_no_bun.save("public/assets/devotee_male.png", "PNG")
print("Saved devotee_male.png")

# 3. Extract devotee_chule.png from thien_canh_backview_raw_1794066988395.jpg
im_stage = Image.open(r"C:\Users\LENOVO\.gemini\antigravity\brain\7d577596-5286-41d1-a416-6dbd86c9fe76\thien_canh_backview_raw_1794066988395.jpg").convert("RGB")
im_stage_1080 = im_stage.resize((1080, 1920), Image.Resampling.LANCZOS)

# Crop Chu Le box:
# In 1080x1920: Chu Le is at x: 340..740, y: 1140..1900
chule_crop = im_stage_1080.crop((340, 1140, 740, 1900))
chule_crop.save("public/assets/chule_crop_raw.png")
print("Saved chule_crop_raw.png for inspection")
