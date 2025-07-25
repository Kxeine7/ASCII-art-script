from PIL import Image

# Define ASCII characters from dark to light
ASCII_CHARS = "@%#*+=-:. "

# Resize image keeping aspect ratio
def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 adjusts for font height
    return image.resize((new_width, new_height))

# Convert image to grayscale
def grayify(image):
    return image.convert("L")

# Map grayscale pixels to ASCII characters
def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "".join(ASCII_CHARS[pixel // 25] for pixel in pixels)
    return ascii_str

# Main function
def image_to_ascii(path, new_width=100):
    try:
        image = Image.open(path)
    except:
        print("Image not found.")
        return

    image = resize_image(image, new_width)
    image = grayify(image)

    ascii_str = pixels_to_ascii(image)
    
    # Format the ASCII string into lines
    pixel_count = len(ascii_str)
    ascii_image = "\n".join(
        ascii_str[i:(i + new_width)] for i in range(0, pixel_count, new_width)
    )

    return ascii_image

# Example usage
ascii_art = image_to_ascii("example.jpg", new_width=100)
print(ascii_art)
