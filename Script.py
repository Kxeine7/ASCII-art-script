from PIL import Image, ImageDraw, ImageFont

# Detailed ASCII character set from darkest to lightest
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZ0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Resize image while preserving aspect ratio
def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 compensates for font squish
    return image.resize((new_width, new_height))

# Convert image to grayscale
def grayify(image):
    return image.convert("L")

# Map each pixel to an ASCII character
def pixels_to_ascii(image):
    pixels = image.getdata()
    scale = 256 // len(ASCII_CHARS)  # Adjust scale based on character count
    ascii_str = "".join(
        [ASCII_CHARS[min(pixel // scale, len(ASCII_CHARS) - 1)] for pixel in pixels]
    )
    return ascii_str

# Convert ASCII string into an image using Pillow
def ascii_to_image(ascii_text, font_path=None, font_size=10, bg_color="white", text_color="black"):
    lines = ascii_text.split("\n")
    max_width = max(len(line) for line in lines)

    # Load font
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

    # Measure character size using textbbox (Pillow ≥10 compatible)
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), "A", font=font)
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]

    # Create image
    img_width = char_width * max_width
    img_height = char_height * len(lines)
    image = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)

    # Draw text line by line
    for i, line in enumerate(lines):
        draw.text((0, i * char_height), line, fill=text_color, font=font)

    return image

# Full process: image -> ASCII -> image -> PNG
def image_to_ascii_png(
    image_path, 
    output_path="ascii_art.png", 
    width=120, 
    font_path=None, 
    font_size=10
):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"❌ Could not open image: {e}")
        return

    image = resize_image(image, new_width=width)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image)

    # Format ASCII string into lines
    ascii_lines = "\n".join(
        ascii_str[i:i + width] for i in range(0, len(ascii_str), width)
    )

    # Convert ASCII to image
    ascii_img = ascii_to_image(
        ascii_lines,
        font_path=font_path,
        font_size=font_size,
        bg_color="white",
        text_color="black"
    )

    # Save as PNG
    ascii_img.save(output_path)
    print(f"✅ ASCII art saved as '{output_path}'")

# === Example Usage ===
image_to_ascii_png(
    image_path="example.jpg",       # Change this to your image file
    output_path="ascii_output.png",
    width=120,
    font_path=None,                 # Optional: add a TTF font path
    font_size=12
)
