from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Image dimensions (OG standard)
WIDTH = 1200
HEIGHT = 630

# Create base image with gradient
img = Image.new('RGB', (WIDTH, HEIGHT))
pixels = img.load()

# Create gradient background
for y in range(HEIGHT):
    for x in range(WIDTH):
        # Diagonal gradient from top-left to bottom-right
        t = (x + y) / (WIDTH + HEIGHT)

        # Colors: #1a1a2e -> #16213e -> #0f3460
        if t < 0.5:
            t2 = t * 2
            r = int(26 + (22 - 26) * t2)
            g = int(26 + (33 - 26) * t2)
            b = int(46 + (62 - 46) * t2)
        else:
            t2 = (t - 0.5) * 2
            r = int(22 + (15 - 22) * t2)
            g = int(33 + (52 - 33) * t2)
            b = int(62 + (96 - 62) * t2)

        pixels[x, y] = (r, g, b)

draw = ImageDraw.Draw(img)

# Try to load fonts, fallback to default
try:
    title_font = ImageFont.truetype("cour.ttf", 72)  # Courier New
except:
    try:
        title_font = ImageFont.truetype("C:/Windows/Fonts/cour.ttf", 72)
    except:
        title_font = ImageFont.load_default()

try:
    subtitle_font = ImageFont.truetype("segoeui.ttf", 32)
except:
    try:
        subtitle_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 32)
    except:
        subtitle_font = ImageFont.load_default()

# Draw title with glow effect
title = "codeweb.com"
title_color = (0, 212, 255)  # #00d4ff

# Get title bounding box for centering
bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = bbox[2] - bbox[0]
title_height = bbox[3] - bbox[1]
title_x = (WIDTH - title_width) // 2
title_y = 230

# Create glow layer
glow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_layer)

# Draw glow (multiple passes with blur)
for i in range(3):
    glow_draw.text((title_x, title_y), title, font=title_font, fill=(0, 212, 255, 100))

glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=15))

# Composite glow onto main image
img = Image.alpha_composite(img.convert('RGBA'), glow_layer)
draw = ImageDraw.Draw(img)

# Draw main title text
draw.text((title_x, title_y), title, font=title_font, fill=title_color)

# Draw divider line
divider_width = 200
divider_height = 4
divider_x = (WIDTH - divider_width) // 2
divider_y = 330

# Gradient divider
for x in range(divider_width):
    t = x / divider_width
    r = int(0 + (123 - 0) * t)
    g = int(212 + (44 - 212) * t)
    b = int(255 + (191 - 255) * t)
    for y in range(divider_height):
        draw.point((divider_x + x, divider_y + y), fill=(r, g, b))

# Draw "COMING SOON" text
subtitle = "COMING SOON"
subtitle_color = (160, 160, 160)  # #a0a0a0

bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = bbox[2] - bbox[0]
subtitle_x = (WIDTH - subtitle_width) // 2
subtitle_y = 380

draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=subtitle_color)

# Save as PNG
output_path = os.path.join(os.path.dirname(__file__), 'og-image.png')
img.convert('RGB').save(output_path, 'PNG')
print(f"Created: {output_path}")
