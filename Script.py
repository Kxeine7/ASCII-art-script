import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Detailed ASCII characters from darkest to lightest
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZ0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def resize_image_pil(image, new_width=150):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))

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

def detect_edges_cv2(image_path, new_width=150):
    # Load with OpenCV in grayscale
    img_cv = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img_cv is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Resize to new_width keeping aspect ratio
    height, width = img_cv.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    img_cv = cv2.resize(img_cv, (new_width, new_height))

    # Detect edges using Canny
    edges = cv2.Canny(img_cv, threshold1=100, threshold2=200)

    # Invert edges to make lines white on black (optional)
    edges_inv = cv2.bitwise_not(edges)

    # Blend edges with original grayscale for contrast enhancement
    blended = cv2.addWeighted(img_cv, 0.7, edges_inv, 0.3, 0)

    return blended

def image_to_ascii_with_edges(image_path, output_path="ascii_edges.png", width=150, font_path=None, font_size=12):
    try:
        # Get enhanced grayscale with edges using OpenCV
        enhanced_gray = detect_edges_cv2(image_path, new_width=width)

        # Convert numpy array to PIL Image
        pil_img = Image.fromarray(enhanced_gray)

    except Exception as e:
        print(f"Error: {e}")
        return

    ascii_str = pixels_to_ascii(pil_img)

    ascii_lines = "\n".join(
        ascii_str[i:i + width] for i in range(0, len(ascii_str), width)
    )

    # Print ASCII art
    print(ascii_lines)

    ascii_img = ascii_to_image(
        ascii_lines,
        font_path=font_path,
        font_size=font_size,
        bg_color="black",
        text_color="white"
    )
    ascii_img.save(output_path)
    print(f"ASCII art with edge detection saved to {output_path}")

# === Example usage ===
image_to_ascii_with_edges(
    image_path="example.jpg",  # Replace with your image path
    output_path="ascii_with_edges.png",
    width=150,
    font_path=None,
    font_size=12
)
