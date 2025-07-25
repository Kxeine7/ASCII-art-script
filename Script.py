from PIL import Image, ImageDraw, ImageFont

# Much more detailed ASCII chars from dark to light
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZ0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def resize_image(image, new_width=150):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    scale = 256 // len(ASCII_CHARS)
    ascii_str = "".join(
        ASCII_CHARS[min(pixel // scale, len(ASCII_CHARS) - 1)] for pixel in pixels
    )
    return ascii_str

def ascii_to_image(ascii_text, font_path=None, font_size=12, bg_color="black", text_color="white"):
    lines = ascii_text.split("\n")
    max_width = max(len(line) for line in lines)

    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), "A", font=font)
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]

    img_width = char_width * max_width
    img_height = char_height * len(lines)

    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(lines):
        draw.text((0, i * char_height), line, fill=text_color, font=font)

    return img

def image_to_ascii_png_and_print(image_path, output_path="ascii_output.png", width=150, font_path=None, font_size=12):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"❌ Error opening image: {e}")
        return

    image = resize_image(image, new_width=width)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image)

    ascii_lines = "\n".join(
        ascii_str[i:i + width] for i in range(0, len(ascii_str), width)
    )

    # Print ASCII art in terminal
    print(ascii_lines)

    ascii_img = ascii_to_image(
        ascii_lines,
        font_path=font_path,
        font_size=font_size,
        bg_color="black",
        text_color="white"
    )
    ascii_img.save(output_path)
    print(f"✅ ASCII art saved as: {output_path}")

# === Example usage ===
image_to_ascii_png_and_print(
    image_path="example.jpg",  # Change to your image path
    output_path="ascii_output.png",
    width=150,
    font_path=None,            # Optional: specify TTF font path
    font_size=12
)
