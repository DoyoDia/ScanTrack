from PIL import Image, ImageDraw, ImageFont

# Create an image with white background
width, height = 200, 100  # example dimensions
image = Image.new('RGB', (width, height), 'white')

# Initialize the drawing context
draw = ImageDraw.Draw(image)

# Specify the font and the text
font = ImageFont.load_default()
text = "Sample Text"

# Get size of the text
text_width, text_height = draw.textsize(text, font=font)

# Display the text size
print(text_width, text_height)
