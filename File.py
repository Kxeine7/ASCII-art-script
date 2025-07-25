from PIL import Image, ImageDraw, ImageFont
import math

def image_to_ascii_png(input_path, output_path, output_width=100):
    # ASCII characters from darkest to lightest
    ascii_chars = "@%#*+=-:. "
    
    # Open and convert image to grayscale
    try:
        img = Image.open(input_path).convert('L')
    except Exception as e:
        print(f"Error opening image: {e}")
        return
    
    # Calculate dimensions
    width, height = img.size
    aspect_ratio = height / width
    output_height = int(aspect_ratio * output_width * 0.55)  # Adjust for font aspect ratio
    
    # Resize image
    img = img.resize((output_width, output_height), Image.Resampling.LANCZOS)
    pixels = img.getdata()
    
    # Convert pixels to ASCII
    ascii_image = []
    for i, pixel in enumerate(pixels):
        # Map pixel value (0-255) to ASCII character
        ascii_index = math.floor(pixel / 255 * (len(ascii_chars) - 1))
        ascii_image.append(ascii_chars[ascii_index])
        if (i + 1) % output_width == 0:
            ascii_image.append('\n')
    
    ascii_text = ''.join(ascii_image)
    
    # Create new image for ASCII art
    font_size = 10
    try:
        # Try to use a monospaced font
        font = ImageFont.truetype("cour.ttf", font_size)  # Courier New
    except:
        # Fallback to default font if courier not available
        font = ImageFont.load_default()
    
    # Calculate text dimensions
    lines = ascii_text.split('\n')
    text_width = max(len(line) for line in lines) * font_size
    text_height = len(lines) * font_size
    
    # Create new black image
    output_img = Image.new('RGB', (text_width, text_height), color='black')
    draw = ImageDraw.Draw(output_img)
    
    # Draw ASCII text in white
    y = 0
    for line in lines:
        draw.text((0, y), line, fill='white', font=font)
        y += font_size
    
    # Save the output image
    try:
        output_img.save(output_path, 'PNG')
        print(f"ASCII art saved to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")

# Example usage
if __name__ == "__main__":
    input_image = "input.jpg"  # Replace with your image path
    output_image = "ascii_output.png"
    image_to_ascii_png(input_image, output_image, output_width=100)
