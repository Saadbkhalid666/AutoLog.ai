from PIL import Image, ImageDraw, ImageFont

# Create a blank white image
img = Image.new("RGB", (400, 200), color="white")

draw = ImageDraw.Draw(img)
draw.text((10, 50), "Litres: 50\nPrice: 4000\nMileage: 12345", fill="black")

# Save it
img.save("uploads/test_receipt.jpg")
