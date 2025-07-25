from PIL import Image, ImageDraw, ImageFont

# More detailed ASCII character set (dark to light)
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Convert pixels to ASCII characters
def map_pixels_to_ascii(image, chars=ASCII_CHARS):
    pixels = image.getdata()
    scale = 255 // (len(chars) - 1)
    ascii_str = "".join([chars[pixel // scale] for pixel in pixels])
    return ascii_str

# Resize while maintaining aspect ratio
def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # Adjust for font height
    return image.resize((new_width, new_height))

# Render ASCII text as image (PNG)
def ascii_to_image(ascii_text, font_path=None, font_size=10, bg_color="white", text_color="black"):
    lines = ascii_text.split("\n")
    max_width = max(len(line) for line in lines)

    # Load font
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
    char_width, char_height = font.getsize("A")

    img_width = char_width * max_width
    img_height = char_height * len(lines)

    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(lines):
        draw.text((0, i * char_height), line, fill=text_color, font=font)

    return img

# Main function
def image_to_ascii_png(image_path, output_path="ascii_art.png", width=100, font_path=None, font_size=10):
    image = Image.open(image_path)
    image = resize_image(image, new_width=width).convert("L")
    ascii_str = map_pixels_to_ascii(image)
    
    # Format ASCII into lines
    ascii_lines = "\n".join(ascii_str[i:i + width] for i in range(0, len(ascii_str), width))

    # Convert ASCII to image and save
    ascii_img = ascii_to_image(ascii_lines, font_path=font_path, font_size=font_size)
    ascii_img.save(output_path)
    print(f"✅ ASCII art saved as: {output_path}")

# Example usage
image_to_ascii_png("example.jpg", output_path="ascii_output.png", width=120, font_size=12)
